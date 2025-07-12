import {StateVariable} from 'impera-js'

// Impera works with localstorage, there is an idea to improve but not yet implemented
localStorage.clear();

let DEFAULT_STATE = {
    visible_section : "generate"
}

export var AppState  = new StateVariable("AppState", DEFAULT_STATE);
