import {LitElement, css, html} from 'lit';
import {customElement, property} from 'lit/decorators.js';
import {litStatesMixin} from 'impera-js'
import { AppState } from './appState';


@customElement('round-button')
export class RoundButton extends LitElement {
  static styles = css`
    button {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: black;
      background: hsl(240 5.3% 58%);
      border: 1px solid hsl(240 5.3% 58%);
    }
    
    button:hover {
      background: hsl(240 5.6% 73%);;
      border: 1px solid hsl(240 5.6% 73%);
    }
    :host([outline]) button {
      border: 1px solid hsl(240 5% 35.5%);
      background: transparent;
      color: white;
    }
    
    :host([outline]) button:hover {
      border: 1px solid hsl(157.8 66.8% 48.9%);
    }
    :host([outline]) button:hover ::slotted(*) {
        color: hsl(157.8 66.8% 48.9%);
    }
    
    :host([active]) button {
      border-color: hsl(157.8 66.8% 48.9%);
    }

    :host([active]) ::slotted(*) {
      color: hsl(157.8 66.8% 48.9%);
    }
  `;

  render() {
    return html`
      <button>
        <slot></slot>
      </button>
    `;
  }

}


@customElement('hiding-section')
export class HidingSection extends litStatesMixin([AppState],LitElement) {
  AppState:any

  @property({ reflect: true })
  name : string = '';

  @property({ reflect: true })
  align : string = 'top';

  render() {
    let v_section = this.AppState.visible_section;
    let css_align = "flex-start";
    if (this.align === "bottom"){
      css_align = "flex-end";
    }
    else if(this.align === "center")
    {
      css_align = this.align
    }
    console.log(this.align)
    console.log(css_align)

    return html`
    <style>
      :host {
        display: ${this.name === v_section ? 'block' : 'none'};
      }
      section {
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
        box-sizing: border-box;
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;#${css_align};
        min-height: 80vh;
      }
    </style>
    
    <section>
      <slot></slot>
    </section>
    `;
  }
}


@customElement('file-input-button')
export class FileInputButton extends LitElement {

  file:File
  file_url:string

  static styles = css`
  :host {
    display: block;
  }
  button {
    font-family: inherit;
    font-size :inherit;
    box-sizing: border-box;
    border-radius: 5%;
    border: 1px solid hsl(240 5% 35.5%);
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.6rem;
  }
  button:hover {
    border: 1px solid hsl(157.8 66.8% 48.9%);
    color:hsl(157.8 66.8% 48.9%);
  }
  button:hover ::slotted(*) {
      color: hsl(157.8 66.8% 48.9%);
  }
  input {
    display: none;
  }
  `;

  render() {
    return html`
      <button @click=${this.load_file}>
        <slot></slot>
      </button>
      <input id="inpt_file" type="file" accept="image/*" @change=${this.handle_change}/>
    `;
  }

  
  load_file() {
    const input:HTMLInputElement = this.shadowRoot.querySelector('#inpt_file');
    input.click();
  }

  handle_change()
  {
    const input:HTMLInputElement = this.shadowRoot.querySelector('#inpt_file');
    this.file = input.files[0];
    this.file_url = URL.createObjectURL(this.file);
  }
}
