const { createApp } = Vue

createApp({
    data() {
        return {
            username: '',
            password: '',
            isLoggedIn: false,
            userRole: null
        }
    },
    methods: {
        async login() {
            try {
                const response = await fetch('/users/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail || 'Credenciales inválidas'}`);
                    return;
                }

                const data = await response.json();

                localStorage.setItem('accessToken', data.access_token);
                localStorage.setItem('tokenType', data.token_type);

                this.isLoggedIn = true
                this.userRole = data.role

            } catch (error) {
                console.error('Error en la solicitud de inicio de sesión: ', error);
                alert('Ocurrió un error al intentar iniciar sesión');
            }
        }
    }
}).mount('#app')