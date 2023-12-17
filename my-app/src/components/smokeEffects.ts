import * as THREE from 'three';

const container = document.getElementById('three-js-container') as HTMLElement;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
container.appendChild(renderer.domElement);

// Add your smoke effect and other Three.js objects here
// ...

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

animate();
