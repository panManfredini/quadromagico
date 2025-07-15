import { AppState } from "./appState";

// navbar button hooks //
const gen_btn = document.getElementById('generate');
const up_btn = document.getElementById('upload');
const gal_btn = document.getElementById('gallery');

function clearActive(){
    gen_btn.removeAttribute("active");
    up_btn.removeAttribute("active");
    gal_btn.removeAttribute("active");
}
gen_btn?.addEventListener('click',()=>{ AppState.value.visible_section = "generate"; clearActive(); gen_btn.setAttribute("active","")})
up_btn?.addEventListener('click',()=>{ AppState.value.visible_section = "upload"; clearActive(); up_btn.setAttribute("active","")})
gal_btn?.addEventListener('click',()=>{ AppState.value.visible_section = "gallery"; clearActive(); gal_btn.setAttribute("active","")})

clearActive();
gen_btn.setAttribute("active","");