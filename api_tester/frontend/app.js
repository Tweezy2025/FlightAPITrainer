class BookingApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000/api';
        this.passengerCount = 0;
        this.init();
    }

    init() {
        // Навигация
        document.getElementById('auth-btn').addEventListener('click', () => this.switchForm('auth'));
        document.getElementById('single-btn').addEventListener('click', () => this.switchForm('single'));
        document.getElementById('bulk-btn').addEventListener('click', () => this.switchForm('bulk'));

        // Формы бронирования
        document.getElementById('single-booking-form').addEventListener('submit', (e) => this.handleSingleBooking(e));
        document.getElementById('bulk-booking-form').addEventListener('submit', (e) => this.handleBulkBooking(e));
        document.getElementById('add-passenger').addEventListener('click', () => this.addPassenger());

        // Формы авторизации
        document.getElementById('register-form').addEventListener('submit', (e) => this.handleRegister(e));
        document.getElementById('login-form').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());

        // Инициализация bulk формы
        this.setupBulkForm();

        // Статус авторизации
        this.updateAuthStatus();
    }

    // ---------- UI переключение форм ----------

    switchForm(type) {
        document.querySelectorAll('.form-container').forEach(f => f.classList.remove('active'));

        if (type === 'auth') {
            document.getElementById('auth-form').classList.add('active');
        } else if (type === 'single') {
            document.getElementById('single-form').classList.add('active');
        } else if (type === 'bulk') {
            document.getElementById('bulk-form').classList.add('active');
        }

        document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
        if (type === 'auth') {
            document.getElementById('auth-btn').classList.add('active');
        } else if (type === 'single') {
            document.getElementById('single-btn').classList.add('active');
        } else if (type === 'bulk') {
            document.getElementById('bulk-btn').classList.add('active');
        }
    }

    // ---------- Bulk форма ----------

    setupBulkForm() {
        const container = document.getElementById('passengers-container');
        container.innerHTML = '';
        this.passengerCount = 0;
        this.addPassenger();
    }

    addPassenger() {
        this.passengerCount++;

        const container = document.getElementById('passengers-container');
        const passengerGroup = document.createElement('div');
        passengerGroup.className = 'passenger-group';

        passengerGroup.innerHTML = `
            <h3>Пассажир ${this.passengerCount}</h3>
            <input type="text" name="name" placeholder="ФИО" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="tel" name="phone" placeholder="Телефон" required>
            <label><input type="checkbox" name="has_luggage"> Багаж</label>

            <select name="seat_preference">
                <option value="">Предпочтение места (не обязательно)</option>
                <option value="window">У окна</option>
                <option value="aisle">У прохода</option>
            </select>

            <button type="button" class="remove-passenger">Удалить</button>
        `;

        passengerGroup.querySelector('.remove-passenger').addEventListener('click', () => {
            passengerGroup.remove();
        });

        container.appendChild(passengerGroup);
    }

    // ---------- Одиночное бронирование ----------

    async handleSingleBooking(event) {
        event.preventDefault();

        const form = event.target;
        const data = {
            flight_number: form.flight_number.value,
            passenger: form.passenger.value,
            email: form.email.value,
            phone: form.phone.value,
            has_luggage: form.has_luggage.checked
        };

        this.sendRequest('/bookings/', data);
    }

    // ---------- Массовое бронирование ----------

    async handleBulkBooking(event) {
        event.preventDefault();

        const form = event.target;
        const passengers = [];

        document.querySelectorAll('#passengers-container .passenger-group').forEach(group => {
            passengers.push({
                name: group.querySelector('input[name="name"]').value,
                email: group.querySelector('input[name="email"]').value,
                phone: group.querySelector('input[name="phone"]').value,
                has_luggage: group.querySelector('input[name="has_luggage"]').checked,
                seat_preference: group.querySelector('select[name="seat_preference"]').value || null
            });
        });

        const data = {
            flight_number: form.flight_number.value,
            promo_code: form.promo_code.value || null,
            notes: form.notes.value || null,
            passengers
        };

        this.sendRequest('/bookings/', data);
    }

    // ---------- Общий метод отправки запросов ----------

    async sendRequest(endpoint, payload) {
        const display = document.getElementById('response-display');
        display.innerHTML = '<p>Загрузка...</p>';

        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = 'Bearer ' + token;
        }

        try {
            const response = await fetch(this.apiBaseUrl + endpoint, {
                method: 'POST',
                headers,
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                display.innerHTML = `<pre class="error">${JSON.stringify(data, null, 2)}</pre>`;
            } else {
                display.innerHTML = `<pre class="success">${JSON.stringify(data, null, 2)}</pre>`;
            }

        } catch (error) {
            display.innerHTML = `<p class="error">Ошибка: ${error.message}</p>`;
        }
    }

    // ---------- Регистрация ----------

    async handleRegister(event) {
        event.preventDefault();
        const form = event.target;

        const payload = {
            email: form.email.value,
            password: form.password.value
        };

        const display = document.getElementById('response-display');
        display.innerHTML = 'Регистрация...';

        try {
            const res = await fetch(this.apiBaseUrl + '/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!res.ok) {
                display.innerHTML = `<pre class="error">${JSON.stringify(data, null, 2)}</pre>`;
                return;
            }

            display.innerHTML = `<pre class="success">Регистрация успешна!</pre>`;
        } catch (err) {
            display.innerHTML = `<p class="error">${err.message}</p>`;
        }
    }

    // ---------- Логин ----------

    async handleLogin(event) {
        event.preventDefault();
        const form = event.target;

        const payload = {
            email: form.email.value,
            password: form.password.value
        };

        const display = document.getElementById('response-display');
        display.innerHTML = 'Вход...';

        try {
            const res = await fetch(this.apiBaseUrl + '/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!res.ok) {
                display.innerHTML = `<pre class="error">${JSON.stringify(data, null, 2)}</pre>`;
                return;
            }

            localStorage.setItem('token', data.access_token);

            display.innerHTML = `<pre class="success">Вход выполнен!</pre>`;
            this.updateAuthStatus();
        } catch (err) {
            display.innerHTML = `<p class="error">${err.message}</p>`;
        }
    }

    // ---------- Logout ----------

    logout() {
        localStorage.removeItem('token');
        this.updateAuthStatus();
        document.getElementById('response-display').innerHTML = '<p>Вы вышли из системы</p>';
    }

    // ---------- Статус авторизации ----------

    updateAuthStatus() {
        const status = document.getElementById('auth-status');
        const logoutBtn = document.getElementById('logout-btn');

        if (localStorage.getItem('token')) {
            status.textContent = 'Авторизован';
            status.classList.add('authenticated');
            logoutBtn.style.display = 'inline-block';
        } else {
            status.textContent = 'Не авторизован';
            status.classList.remove('authenticated');
            logoutBtn.style.display = 'none';
        }
    }
}

new BookingApp();
