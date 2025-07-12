import { AppState } from "./appState";

// navbar button hooks //
const gen_btn = document.getElementById('generate');
const up_btn = document.getElementById('upload');
const gal_btn = document.getElementById('gallery');

gen_btn?.addEventListener('click',()=>{ AppState.value.visible_section = "generate"})
up_btn?.addEventListener('click',()=>{ AppState.value.visible_section = "upload"})
gal_btn?.addEventListener('click',()=>{ AppState.value.visible_section = "gallery"})