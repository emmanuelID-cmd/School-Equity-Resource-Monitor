const header = document.createElement('header');
header.className = 'product-header';
header.innerHTML = '<a class="brand" href="index.html"><img src="school-equity-resource-monitor-mockup/logo-modern-school-flat.svg" alt="School Equity Resource Monitor logo"><span><strong>School Equity Resource Monitor</strong><small>Move from observed patterns to documented review questions, assigned actions, and follow-up evidence.</small></span></a><span class="framing">Observational evidence — not causal proof.</span>';
document.body.prepend(header);
const nav = document.querySelector('.nav');
if (nav) {
  const leftHint = document.createElement('span');
  const rightHint = document.createElement('span');
  leftHint.className = 'nav-scroll-hint nav-scroll-left';
  rightHint.className = 'nav-scroll-hint nav-scroll-right';
  leftHint.setAttribute('aria-hidden', 'true'); rightHint.setAttribute('aria-hidden', 'true');
  leftHint.textContent = '‹'; rightHint.textContent = '›';
  const cueStyle = 'position:fixed;top:110px;z-index:100;padding:8px 10px;color:#d8edf9;background:#172033;font-size:22px;line-height:22px;pointer-events:none;display:none;';
  leftHint.style.cssText = `${cueStyle}left:0;`;
  rightHint.style.cssText = `${cueStyle}right:0;`;
  nav.append(leftHint, rightHint);
  const updateHint = () => { const mobile = window.matchMedia('(max-width: 700px)').matches; const right = nav.scrollWidth - nav.clientWidth - nav.scrollLeft > 4; const left = nav.scrollLeft > 4; leftHint.style.display = mobile && left ? 'block' : 'none'; rightHint.style.display = mobile && right ? 'block' : 'none'; leftHint.classList.toggle('visible', mobile && left); rightHint.classList.toggle('visible', mobile && right); };
  nav.addEventListener('scroll', updateHint, { passive: true });
  window.addEventListener('resize', updateHint);
  requestAnimationFrame(updateHint);
}
