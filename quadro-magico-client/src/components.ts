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
      border: 1px solid hsl(240 5% 35.5%);
      background: transparent;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    button:hover {
      border: 1px solid hsl(157.8 66.8% 48.9%);
    }
    button:hover ::slotted(*) {
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
        align-items: ${css_align};
        min-height: 80vh;
      }
    </style>
    
    <section>
      <slot></slot>
    </section>
    `;
  }
}