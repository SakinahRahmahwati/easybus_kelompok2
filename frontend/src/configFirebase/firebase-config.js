// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAKZ5GVZscNjzNrv9hc4LbFbPHp5izDFxI",
  authDomain: "easybus-83d10.firebaseapp.com",
  projectId: "easybus-83d10",
  storageBucket: "easybus-83d10.appspot.com",
  messagingSenderId: "185187224438",
  appId: "1:185187224438:web:f13c686e301182a046c857"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

export { storage };