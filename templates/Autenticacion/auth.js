// Configuración de Firebase
import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";

const firebaseConfig = {
    apiKey: "TU_API_KEY",
    authDomain: "TU_AUTH_DOMAIN",
    projectId: "TU_PROJECT_ID",
    storageBucket: "TU_STORAGE_BUCKET",
    messagingSenderId: "TU_MESSAGING_SENDER_ID",
    appId: "TU_APP_ID"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Función de Registro
async function register() {
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;
    const message = document.getElementById("registerMessage");

    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        message.textContent = "Registro exitoso. Por favor, inicia sesión.";
    } catch (error) {
        console.error("Error en el registro:", error);
        message.textContent = "Error en el registro: " + error.message;
    }
}

// Función de Inicio de Sesión
async function login() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const message = document.getElementById("loginMessage");

    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const token = await userCredential.user.getIdToken();
        
        // Enviar token a Flask para autenticación
        fetch("URL_DE_TU_BACKEND/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ token })
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                message.textContent = "Inicio de sesión exitoso.";
                localStorage.setItem("jwt", data.access_token); // Guardar el JWT en el almacenamiento local
            } else {
                message.textContent = "Error de autenticación en el servidor.";
            }
        })
        .catch(error => {
            console.error("Error en el servidor:", error);
            message.textContent = "Error en el servidor.";
        });
    } catch (error) {
        console.error("Error en el inicio de sesión:", error);
        message.textContent = "Error en el inicio de sesión: " + error.message;
    }
}
