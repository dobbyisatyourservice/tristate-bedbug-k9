(function(){
  // mobile menu
  var btn=document.getElementById('menu-btn'), nav=document.getElementById('site-nav');
  if(btn&&nav){btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');});}

  // preview mode: hash routing between views (only present in the single-file preview)
  var views=document.querySelectorAll('.view');
  if(views.length){
    var show=function(){
      var raw=(location.hash||'#home').slice(1), key=raw, anchor=null;
      if(!document.querySelector('.view[data-view="'+key+'"]')){
        var el=document.getElementById(raw); var v=el&&el.closest('.view');
        if(v){key=v.getAttribute('data-view');anchor=el;} else key='home';
      }
      views.forEach(function(v){v.hidden=v.getAttribute('data-view')!==key;});
      document.querySelectorAll('#site-nav a').forEach(function(a){
        if(a.getAttribute('data-route')===key)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
      if(nav)nav.classList.remove('open');
      if(anchor)anchor.scrollIntoView(); else window.scrollTo(0,0);
    };
    window.addEventListener('hashchange',show); show();
  }

  // forms: in the preview there is nowhere to send, so show the confirmation instead
  document.querySelectorAll('form.form').forEach(function(f){
    f.addEventListener('submit',function(e){
      if(f.hasAttribute('data-netlify')&&location.protocol.indexOf('http')===0&&!views.length)return; // real site: let the host handle it
      e.preventDefault(); var m=f.querySelector('.form-msg'); if(m)m.hidden=false; f.reset();
    });
  });

  // registry search + state filter
  var table=document.getElementById('team-table');
  if(table){
    var q=document.getElementById('team-search'), chips=document.querySelectorAll('.chip'), empty=document.getElementById('team-empty'), state='ALL';
    var run=function(){
      var term=(q.value||'').trim().toLowerCase(), shown=0;
      table.querySelectorAll('tbody tr').forEach(function(r){
        var ok=(state==='ALL'||r.getAttribute('data-state')===state)&&(!term||r.textContent.toLowerCase().indexOf(term)>-1);
        r.hidden=!ok; if(ok)shown++;});
      if(empty)empty.hidden=shown>0;
    };
    q.addEventListener('input',run);
    chips.forEach(function(c){c.addEventListener('click',function(){
      state=c.getAttribute('data-state'); chips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false');}); run();});});
    run();
  }
})();
(function(){
  var c=document.getElementById('cookie'); if(!c)return;
  var link=c.querySelector('[data-route-link]'); if(link&&document.querySelector('.view'))link.setAttribute('href','#privacy');
  var seen=false; try{seen=localStorage.getItem('tsk9-cookie-ok')==='1';}catch(e){}
  if(!seen)c.hidden=false;
  document.getElementById('cookie-ok').addEventListener('click',function(){c.hidden=true;try{localStorage.setItem('tsk9-cookie-ok','1');}catch(e){}});
})();
