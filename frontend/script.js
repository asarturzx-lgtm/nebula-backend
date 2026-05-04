const API_URL = 'http://127.0.0.1:8000/api/v1';
let authToken = '';

// Механизм лампы
document.getElementById('main-pull-cord').addEventListener('click', () => {
    document.body.classList.toggle('light-on');
    // Звуковой эффект клика можно добавить тут
});

// Авторизация
async function login() {
    const pass = document.getElementById('login-input').value;
    if(!pass) return;
    authToken = pass;

    try {
        const res = await fetch(`${API_URL}/users/me`, {
            headers: {'Authorization': `Bearer ${authToken}`}
        });
        if(res.ok) {
            const user = await res.json();
            document.getElementById('user-display').innerText = user.login.toUpperCase();
            document.getElementById('auth-scene').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            startClock();
            refreshData();
        } else { alert("КЛЮЧ ОТКЛОНЕН"); }
    } catch(e) { alert("ОШИБКА СИСТЕМЫ"); }
}

// Обновление данных
async function refreshData() {
    const headers = {'Authorization': `Bearer ${authToken}`};

    const resB = await fetch(`${API_URL}/balance`, {headers});
    const bData = await resB.json();
    document.getElementById('total-balance').innerText = bData.balance.toLocaleString() + " ₽";

    const resW = await fetch(`${API_URL}/wallets_list`, {headers});
    const wallets = await resW.json();

    const select = document.getElementById('op-wallet-name');
    const list = document.getElementById('wallets-list');
    select.innerHTML = ''; list.innerHTML = '';

    wallets.forEach(w => {
        const opt = document.createElement('option');
        opt.value = w.name; opt.innerText = w.name;
        select.appendChild(opt);

        const row = document.createElement('div');
        row.className = 'wallet-item';
        row.style = "display:flex; justify-content:space-between; padding:15px; border-bottom:1px solid #261f1c";
        row.innerHTML = `<span>${w.name}</span><strong style="color:var(--amber)">${w.balance.toLocaleString()} ₽</strong>`;
        list.appendChild(row);
    });
}

// Операции
async function handleOperation(type) {
    const wallet_name = document.getElementById('op-wallet-name').value;
    const amount = document.getElementById('op-amount').value;
    if(!amount) return;

    await fetch(`${API_URL}/operations/${type}`, {
        method: 'POST',
        headers: {'Authorization': `Bearer ${authToken}`, 'Content-Type': 'application/json'},
        body: JSON.stringify({wallet_name, amount, destination: "Vault Transfer"})
    });
    refreshData();
}

async function createWallet() {
    const name = document.getElementById('new-wallet-name').value;
    const balance = document.getElementById('new-wallet-balance').value;
    if(!name) return;

    await fetch(`${API_URL}/wallets`, {
        method: 'POST',
        headers: {'Authorization': `Bearer ${authToken}`, 'Content-Type': 'application/json'},
        body: JSON.stringify({name, initial_balance: balance || 0})
    });
    refreshData();
}

function startClock() {
    setInterval(() => {
        document.getElementById('clock').innerText = new Date().toLocaleTimeString();
    }, 1000);
}

function logout() { location.reload(); }