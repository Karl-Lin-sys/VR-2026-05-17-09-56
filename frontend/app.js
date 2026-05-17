import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { VRButton } from 'three/addons/webxr/VRButton.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { VRMLoaderPlugin, VRMUtils } from '@pixiv/three-vrm';

// --- Scene Setup ---
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight, 0.1, 20.0);
camera.position.set(0.0, 1.4, 1.5);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.xr.enabled = true; // Enable WebXR
document.body.appendChild(renderer.domElement);
document.body.appendChild(VRButton.createButton(renderer)); // Add VR Button

const controls = new OrbitControls(camera, renderer.domElement);
controls.screenSpacePanning = true;
controls.target.set(0.0, 1.4, 0.0);
controls.update();

// Lights
const light = new THREE.DirectionalLight(0xffffff, 1.0);
light.position.set(1.0, 1.0, 1.0).normalize();
scene.add(light);
const ambientLight = new THREE.AmbientLight(0x404040, 1.5); // Soft white light
scene.add(ambientLight);

// --- VRM Loading ---
let currentVrm = null;
const loader = new GLTFLoader();
loader.crossOrigin = 'anonymous';

loader.register((parser) => {
    return new VRMLoaderPlugin(parser);
});

// A dummy VRM URL for demonstration (replace with actual model)
const VRM_URL = 'https://pixiv.github.io/three-vrm/packages/three-vrm/examples/models/VRM1_Constraint_Twist_Sample.vrm'; 

loader.load(
    VRM_URL,
    (gltf) => {
        const vrm = gltf.userData.vrm;
        VRMUtils.removeUnnecessaryJoints(gltf.scene);
        scene.add(vrm.scene);
        currentVrm = vrm;
        
        // Fix rotation
        vrm.scene.rotation.y = Math.PI; 
        
        console.log('VRM loaded successfully');
    },
    (progress) => console.log('Loading model...', 100.0 * (progress.loaded / progress.total), '%'),
    (error) => console.error(error)
);

// --- Animation Loop ---
const clock = new THREE.Clock();

function animate() {
    renderer.setAnimationLoop(() => {
        const deltaTime = clock.getDelta();
        if (currentVrm) {
            currentVrm.update(deltaTime);
        }
        renderer.render(scene, camera);
    });
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- AI Chat & Security Integration ---
const sendBtn = document.getElementById('send-btn');
const inputField = document.getElementById('user-input');
const chatLog = document.getElementById('chat-log');

async function sendMessage() {
    const text = inputField.value.trim();
    if (!text) return;
    
    appendMessage('You', text);
    inputField.value = '';
    
    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: "master_user_001", // Authentication
                message: text
            })
        });
        
        if (!response.ok) {
            if (response.status === 403) {
                appendMessage('System', 'Security Alert: Unauthorized access.');
            } else {
                appendMessage('System', 'Server error.');
            }
            return;
        }
        
        const data = await response.json();
        appendMessage('Anya', data.reply);
        
        // Self-Regulation: Update VRM Expression based on backend state
        if (currentVrm) {
            currentVrm.expressionManager.setValue('happy', 0);
            currentVrm.expressionManager.setValue('angry', 0);
            currentVrm.expressionManager.setValue('sad', 0);
            currentVrm.expressionManager.setValue('surprised', 0); // using standard VRM expressions
            
            if (data.emotion === 'happy') currentVrm.expressionManager.setValue('happy', 1);
            if (data.emotion === 'angry') currentVrm.expressionManager.setValue('angry', 1);
            if (data.emotion === 'embarrassed') currentVrm.expressionManager.setValue('surprised', 0.5); 
        }
        
    } catch (err) {
        console.error(err);
        appendMessage('System', 'Failed to connect to AI Core.');
    }
}

function appendMessage(sender, message) {
    const div = document.createElement('div');
    div.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
