(function(){try{var g=true,k=null,l=false,n,o=this,aa=function(a){a.D=function(){return a.Ba||(a.Ba=new a)}},p=function(a){var b=typeof a;if(b=="object")if(a){if(a instanceof Array)return"array";else if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if(c=="[object Window]")return"object";if(c=="[object Array]"||typeof a.length=="number"&&typeof a.splice!="undefined"&&typeof a.propertyIsEnumerable!="undefined"&&!a.propertyIsEnumerable("splice"))return"array";if(c=="[object Function]"||typeof a.call!=
"undefined"&&typeof a.propertyIsEnumerable!="undefined"&&!a.propertyIsEnumerable("call"))return"function"}else return"null";else if(b=="function"&&typeof a.call=="undefined")return"object";return b},ca=function(a){var b=p(a);return b=="array"||b=="object"&&typeof a.length=="number"},q=function(a){return typeof a=="string"},da=function(a){var b=typeof a;return b=="object"&&a!=k||b=="function"},ea=function(a){return a.call.apply(a.bind,arguments)},fa=function(a,b){if(!a)throw Error();if(arguments.length>
2){var c=Array.prototype.slice.call(arguments,2);return function(){var d=Array.prototype.slice.call(arguments);Array.prototype.unshift.apply(d,c);return a.apply(b,d)}}else return function(){return a.apply(b,arguments)}},r=function(){r=Function.prototype.bind&&Function.prototype.bind.toString().indexOf("native code")!=-1?ea:fa;return r.apply(k,arguments)},ga=function(a){var b=Array.prototype.slice.call(arguments,1);return function(){var c=Array.prototype.slice.call(arguments);c.unshift.apply(c,b);
return a.apply(this,c)}},ha=Date.now||function(){return+new Date},t=function(a,b){var c=a.split("."),d=o;!(c[0]in d)&&d.execScript&&d.execScript("var "+c[0]);for(var e;c.length&&(e=c.shift());)if(!c.length&&b!==undefined)d[e]=b;else d=d[e]?d[e]:d[e]={}};window.gbar.tev&&window.gbar.tev(3,"m");var pa=function(a){if(!ia.test(a))return a;if(a.indexOf("&")!=-1)a=a.replace(la,"&amp;");if(a.indexOf("<")!=-1)a=a.replace(ma,"&lt;");if(a.indexOf(">")!=-1)a=a.replace(na,"&gt;");if(a.indexOf('"')!=-1)a=a.replace(oa,"&quot;");return a},la=/&/g,ma=/</g,na=/>/g,oa=/\"/g,ia=/[&<>\"]/,qa=function(a,b){if(a<b)return-1;else if(a>b)return 1;return 0};var v=Array.prototype,ra=v.indexOf?function(a,b,c){return v.indexOf.call(a,b,c)}:function(a,b,c){c=c==k?0:c<0?Math.max(0,a.length+c):c;if(q(a)){if(!q(b)||b.length!=1)return-1;return a.indexOf(b,c)}for(;c<a.length;c++)if(c in a&&a[c]===b)return c;return-1},sa=v.forEach?function(a,b,c){v.forEach.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=q(a)?a.split(""):a,f=0;f<d;f++)f in e&&b.call(c,e[f],f,a)},ta=v.filter?function(a,b,c){return v.filter.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=[],
f=0,h=q(a)?a.split(""):a,i=0;i<d;i++)if(i in h){var j=h[i];if(b.call(c,j,i,a))e[f++]=j}return e},ua=function(){return v.concat.apply(v,arguments)},va=function(a){if(p(a)=="array")return ua(a);else{for(var b=[],c=0,d=a.length;c<d;c++)b[c]=a[c];return b}},wa=function(a,b,c){return arguments.length<=2?v.slice.call(a,b):v.slice.call(a,b,c)};var xa=function(a,b){this.x=a!==undefined?a:0;this.y=b!==undefined?b:0};var ya=function(a,b){this.width=a;this.height=b};var za=function(a,b){for(var c in a)b.call(void 0,a[c],c,a)},Aa=["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"],Ba=function(a){for(var b,c,d=1;d<arguments.length;d++){c=arguments[d];for(b in c)a[b]=c[b];for(var e=0;e<Aa.length;e++){b=Aa[e];if(Object.prototype.hasOwnProperty.call(c,b))a[b]=c[b]}}};var w,Ca,Da,Ea,Fa,Ga=function(){return o.navigator?o.navigator.userAgent:k};Fa=Ea=Da=Ca=w=l;var y;if(y=Ga()){var Ha=o.navigator;w=y.indexOf("Opera")==0;Ca=!w&&y.indexOf("MSIE")!=-1;Ea=(Da=!w&&y.indexOf("WebKit")!=-1)&&y.indexOf("Mobile")!=-1;Fa=!w&&!Da&&Ha.product=="Gecko"}var z=Ca,Na=Fa,Oa=Da,Pa=Ea,Qa;
a:{var Ra="",A;if(w&&o.opera){var Sa=o.opera.version;Ra=typeof Sa=="function"?Sa():Sa}else{if(Na)A=/rv\:([^\);]+)(\)|;)/;else if(z)A=/MSIE\s+([^\);]+)(\)|;)/;else if(Oa)A=/WebKit\/(\S+)/;if(A){var Ta=A.exec(Ga());Ra=Ta?Ta[1]:""}}if(z){var Ua,Va=o.document;Ua=Va?Va.documentMode:undefined;if(Ua>parseFloat(Ra)){Qa=String(Ua);break a}}Qa=Ra}
var Wa=Qa,Xa={},Ya=function(a){var b;if(!(b=Xa[a])){b=0;for(var c=String(Wa).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),d=String(a).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),e=Math.max(c.length,d.length),f=0;b==0&&f<e;f++){var h=c[f]||"",i=d[f]||"",j=RegExp("(\\d*)(\\D*)","g"),m=RegExp("(\\d*)(\\D*)","g");do{var s=j.exec(h)||["","",""],x=m.exec(i)||["","",""];if(s[0].length==0&&x[0].length==0)break;b=qa(s[1].length==0?0:parseInt(s[1],10),x[1].length==0?0:parseInt(x[1],10))||qa(s[2].length==
0,x[2].length==0)||qa(s[2],x[2])}while(b==0)}b=Xa[a]=b>=0}return b},Za={},$a=function(){return Za[9]||(Za[9]=z&&!!document.documentMode&&document.documentMode>=9)};var ab=!z||$a(),bb=!Na&&!z||z&&$a()||Na&&Ya("1.9.1");z&&Ya("9");var cb=function(a){var b;b=a.className;b=q(b)&&b.match(/\S+/g)||[];for(var c=wa(arguments,1),d=b.length+c.length,e=0;e<c.length;e++)ra(b,c[e])>=0||b.push(c[e]);a.className=b.join(" ");return b.length==d};var eb=function(a,b){za(b,function(c,d){if(d=="style")a.style.cssText=c;else if(d=="class")a.className=c;else if(d=="for")a.htmlFor=c;else if(d in db)a.setAttribute(db[d],c);else if(d.lastIndexOf("aria-",0)==0)a.setAttribute(d,c);else a[d]=c})},db={cellpadding:"cellPadding",cellspacing:"cellSpacing",colspan:"colSpan",rowspan:"rowSpan",valign:"vAlign",height:"height",width:"width",usemap:"useMap",frameborder:"frameBorder",maxlength:"maxLength",type:"type"},gb=function(){var a=arguments,b=a[0],c=a[1];
if(!ab&&c&&(c.name||c.type)){b=["<",b];c.name&&b.push(' name="',pa(c.name),'"');if(c.type){b.push(' type="',pa(c.type),'"');var d={};Ba(d,c);c=d;delete c.type}b.push(">");b=b.join("")}b=document.createElement(b);if(c)if(q(c))b.className=c;else p(c)=="array"?cb.apply(k,[b].concat(c)):eb(b,c);a.length>2&&fb(document,b,a,2);return b},fb=function(a,b,c,d){function e(i){if(i)b.appendChild(q(i)?a.createTextNode(i):i)}for(;d<c.length;d++){var f=c[d];if(ca(f)&&!(da(f)&&f.nodeType>0)){var h;a:{if(f&&typeof f.length==
"number")if(da(f)){h=typeof f.item=="function"||typeof f.item=="string";break a}else if(p(f)=="function"){h=typeof f.item=="function";break a}h=l}sa(h?va(f):f,e)}else e(f)}},hb=function(a){fb(a.nodeType==9?a:a.ownerDocument||a.document,a,arguments,1)},ib=function(a){if(bb&&a.children!=undefined)return a.children;return ta(a.childNodes,function(b){return b.nodeType==1})};var jb=function(a){jb[" "](a);return a};jb[" "]=function(){};var B=window.gbar;var C=function(a,b,c){var d={};d._sn=["m",b,c].join(".");B.logger.ml(a,d)};var G={ka:1,ab:2,$a:3,na:4,ma:5,pa:6,oa:7,la:8};var kb=[],lb=k,H=function(a,b){kb.push([a,b])},I=function(a,b){var c=k;if(b)c={m:b};B.tev&&B.tev(a,"m",c)};var mb,Bb=function(){nb();t("gbar.addHover",ob);t("gbar.close",pb);t("gbar.cls",qb);t("gbar.tg",zb);B.adh("gbd4",function(){Ab(5,!J)});B.adh("gbd5",function(){Ab(6,!J)})},K=function(){if(mb===undefined)mb=/MSIE (\d+)\.(\d+);/.exec(navigator.userAgent);return mb},Cb=function(){var a=K();return a&&a.length>1?new Number(a[1]):k},L="",J=undefined,Db=undefined,Eb=undefined,Fb=undefined,Gb=l,Hb=undefined,Ib=["gbzt","gbgt","gbg0l","gbmt","gbml1","gbqfb","gbqfqw"],M=function(a,b,c,d){var e="on"+b;if(a.addEventListener)a.addEventListener(b,
c,!!d);else if(a.attachEvent)a.attachEvent(e,c);else{var f=a[e];a[e]=function(){var h=f.apply(this,arguments),i=c.apply(this,arguments);return h==undefined?i:i==undefined?h:i&&h}}},O=function(a){return document.getElementById(a)},Jb=function(a){a.preventDefault&&a.preventDefault();a.returnValue=l;a.cancelBubble=g},Kb=function(){var a=O("gbx1");return B.kn&&B.kn()&&a?a.clientWidth:document.documentElement&&document.documentElement.clientWidth?document.documentElement.clientWidth:document.body.clientWidth},
P=function(a){var b={};if(a.style.display!="none"){b.width=a.offsetWidth;b.height=a.offsetHeight;return b}var c=a.style,d=c.display,e=c.visibility,f=c.position;c.visibility="hidden";c.position="absolute";c.display="inline";var h;h=a.offsetWidth;a=a.offsetHeight;c.display=d;c.position=f;c.visibility=e;b.width=h;b.height=a;return b},Lb=function(a){if(Eb===undefined){var b=document.body.style;Eb=!(b.WebkitBoxShadow!==undefined||b.MozBoxShadow!==undefined||b.boxShadow!==undefined||b.BoxShadow!==undefined)}if(Eb){b=
a.id+"-gbxms";var c=O(b);if(!c){c=document.createElement("span");c.id=b;c.className="gbxms";a.appendChild(c)}if(Fb===undefined)Fb=c.offsetHeight<a.offsetHeight/2;if(Fb){c.style.height=a.offsetHeight-5+"px";c.style.width=a.offsetWidth-3+"px"}}},Mb=function(a,b){if(a){var c=a.style,d=b||O(L);if(d){a.parentNode&&a.parentNode.appendChild(d);d=d.style;d.width=a.offsetWidth+"px";d.height=a.offsetHeight+"px";d.left=c.left;d.right=c.right}}},R=function(a){try{if(J){if(B.eh[J]){var b;var c=a||window.event;
b=c?c.ctrlKey||c.metaKey||c.which==2?g:l:l;if(b)return}var d=O(L);if(d){d.style.cssText="";d.style.visibility="hidden"}var e=O(J);if(e){e.style.cssText="";e.style.visibility="hidden";var f=e.getAttribute("aria-owner"),h=f?O(f):k;if(h){Q(h.parentNode,"gbto");h.blur()}}if(Db){Db();Db=undefined}var i=B.ch[J];if(i){a=0;for(var j;j=i[a];a++)try{j()}catch(m){C(m,"sb","cdd1")}}J=undefined}}catch(s){C(s,"sb","cdd2")}},Nb=function(a,b){try{if(J)for(var c=b.target||b.srcElement;c.tagName.toLowerCase()!="a";){if(c.id==
a){b.cancelBubble=g;return c}c=c.parentNode}}catch(d){C(d,"sb","kdo")}return k},Ab=function(a,b){var c={s:b?"o":"c"};a!=-1&&B.logger.il(a,c)},V=function(a,b){var c=a.className;S(a,b)||(a.className+=(c!=""?" ":"")+b)},Q=function(a,b){var c=a.className,d=RegExp("\\s?\\b"+b+"\\b");if(c&&c.match(d))a.className=c.replace(d,"")},S=function(a,b){var c=a.className;return!!(c&&c.match(RegExp("\\b"+b+"\\b")))},zb=function(a,b,c,d){try{a=a||window.event;c=c||l;if(!L){var e=document.createElement("iframe");e.frameBorder=
"0";e.tabIndex="-1";L=e.id="gbs";e.src="javascript:''";O("gbw").appendChild(e)}if(!Gb){M(document,"click",pb);M(document,"keyup",Ob);Gb=g}if(!c){a.preventDefault&&a.preventDefault();a.returnValue=l;a.cancelBubble=g}if(!b){b=a.target||a.srcElement;for(var f=b.parentNode.id;!S(b.parentNode,"gbt");){if(f=="gb")return;b=b.parentNode;f=b.parentNode.id}}var h=b.getAttribute("aria-owns");if(h.length){d||b.focus();if(J==h)qb(h);else{var i=b.offsetWidth;a=0;do a+=b.offsetLeft||0;while(b=b.offsetParent);if(Hb===
undefined){var j=document.body,m,s=document.defaultView;if(s&&s.getComputedStyle){var x=s.getComputedStyle(j,"");if(x)m=x.direction}else m=j.currentStyle?j.currentStyle.direction:j.style.direction;Hb=m=="rtl"}j=Hb?l:g;b=Hb?l:g;if(h=="gbd")b=!b;if(h=="gbz"){b=!b;j=!j}J&&R();var u=B.bh[h];if(u)for(var D=0,E;E=u[D];D++)try{E()}catch(Ia){C(Ia,"sb","t1")}u=a;var F=O(h);if(F){var N=F.style,ja=F.offsetWidth;if(ja<i){N.width=i+"px";ja=i;var T=F.offsetWidth;if(T!=i)N.width=i-(T-i)+"px"}T=5;if(u<0){var ba=
Kb(),Ja;m=window;var Ka=m.document;if(Oa&&!Ya("500")&&!Pa){if(typeof m.innerHeight=="undefined")m=window;var La=m.innerHeight,vc=m.document.documentElement.scrollHeight;if(m==m.top)if(vc<La)La-=15;Ja=new ya(m.innerWidth,La)}else{var rb=Ka.compatMode=="CSS1Compat"?Ka.documentElement:Ka.body;Ja=new ya(rb.clientWidth,rb.clientHeight)}T-=ba-Ja.width}var ka,U;ba=Kb();if(b){ka=j?Math.max(ba-u-ja,T):ba-u-i;U=-(ba-u-i-ka);if(K()){var sb=Cb();if(sb==6||sb==7&&document.compatMode=="BackCompat")U-=2}}else{ka=
j?u:Math.max(u+i-ja,T);U=ka-u}var tb=O("gbw"),ub=O("gb");if(tb&&ub){var vb=tb.offsetLeft;if(vb!=ub.offsetLeft)U-=vb}Lb(F);N.right=b?U+"px":"auto";N.left=b?"auto":U+"px";N.visibility="visible";var wb=F.getAttribute("aria-owner"),xb=wb?O(wb):k;xb&&V(xb.parentNode,"gbto");var Ma=O(L);if(Ma){Mb(F,Ma);Ma.style.visibility="visible"}J=h}var yb=B.dh[h];if(yb)for(D=0;E=yb[D];D++)try{E()}catch(wc){C(wc,"sb","t2")}}}}catch(xc){C(xc,"sb","t3")}},Ob=function(a){if(J)try{a=a||window.event;var b=a.target||a.srcElement;
if(a.keyCode&&b)if(a.keyCode&&a.keyCode==27)R();else if(b.tagName.toLowerCase()=="a"&&b.className.indexOf("gbgt")!=-1&&(a.keyCode==13||a.keyCode==3)){var c=document.getElementById(J);if(c&&c.id!="gbz"){var d=c.getElementsByTagName("a");d&&d.length&&d[0].focus&&d[0].focus()}}}catch(e){C(e,"sb","kuh")}},nb=function(){var a=O("gb");if(a){Q(a,"gbpdjs");var b=a.getElementsByTagName("a");a=[];for(var c=O("gbqfw"),d=0,e;e=b[d];d++)a.push(e);if(c){b=O("gbqfqw");d=c.getElementsByTagName("button");c=[];b&&
c.push(b);if(d&&d.length>0)for(b=0;e=d[b];b++)c.push(e);for(d=0;b=c[d];d++)a.push(b)}for(d=0;c=a[d];d++)(b=Pb(c))&&W(c,ga(Qb,b))}},ob=function(a){var b=Pb(a);b&&W(a,ga(Qb,b))},Pb=function(a){for(var b=0,c;c=Ib[b];b++)if(S(a,c))return c},Rb=function(a){a=a.relatedTarget;var b;a:{try{jb(a.parentNode);b=g;break a}catch(c){}b=l}if(b)return a;return k},W=function(a,b,c){b=function(d,e){return function(f){try{f=f||window.event;var h=Rb(f);d===h||Sb(d,h)||e(f,d)}catch(i){C(i,"sb","bhe")}}}(a,b);if(c)M(a,
c,b);else{M(a,"mouseover",b);M(a,"mouseout",b)}},Qb=function(a,b,c){try{a+="-hvr";if(b.type=="mouseover"){V(c,a);var d=document.activeElement;if(d){var e=S(d,"gbgt")||S(d,"gbzt"),f=S(c,"gbgt")||S(c,"gbzt");e&&f&&d.blur()}}else b.type=="mouseout"&&Q(c,a)}catch(h){C(h,"sb","moaoh")}},Sb=function(a,b){if(a===b)return l;for(;b&&b!==a;)b=b.parentNode;return b===a},Tb=function(a){for(;a&&a.hasChildNodes();)a.removeChild(a.firstChild)},pb=function(a){R(a)},qb=function(a){a==J&&R()},X=function(a,b){var c=
document.createElement(a);c.className=b;return c},Ub=function(a){if(a&&a.style.visibility=="visible"){Lb(a);Mb(a)}},Vb=function(a,b){if(b>=0)return window.setTimeout(a,b);else{a();return 0}};H("base",{init:function(a){Bb(a)}});var Y=function(a){t("gbar.pcm",r(this.ra,this));t("gbar.paa",r(this.qa,this));t("gbar.prm",r(this.Oa,this));t("gbar.pge",r(this.R,this));t("gbar.ppe",r(this.ba,this));t("gbar.spn",r(this.Qa,this));t("gbar.spp",r(this.Ra,this));t("gbar.spd",r(this.Ta,this));this.ga=this.H=this.M=l;this.va=a.mg||"%1$s";this.ua=a.md||"%1$s";this.ya=a.g;this.wa=a.d;this.v=a.e;this.F=a.p;this.xa=a.m;var b=O("gbi4i");b&&b.loadError&&this.R();(b=O("gbmpi"))&&b.loadError&&this.ba();if(!this.M){b=O("gbd4");var c=O("gbmp2"),
d=O("gbmpsb");b&&M(b,"click",r(Nb,this,"gbd4"),g);if(c&&d){M(c,"click",r(this.ia,this));M(d,"click",r(this.ia,this))}this.M=g}if(!this.wa)if((b=O("gbmpn"))&&(b.firstChild&&b.firstChild.nodeValue?b.firstChild.nodeValue:"")==this.v){b=this.v.indexOf("@");b>=0&&Wb(this,this.v.substring(0,b))}if(this.ya){b=O("gbpm");c=O("gbpms");if(b&&c){var e=c.innerHTML.split("%1$s");if(e.length==2){d=document.createTextNode(e[0]);e=document.createTextNode(e[1]);var f=X("span","gbpms2"),h=document.createTextNode(this.xa);
Tb(c);f.appendChild(h);c.appendChild(d);c.appendChild(f);c.appendChild(e);b.style.display=""}}}if(a.xp){a=O("gbg4");b=O("gbg6");a&&M(a,"mouseover",r(this.K,this));b&&M(b,"mouseover",r(this.K,this))}};
Y.prototype.ia=function(a){try{a=a||window.event;a.cancelBubble=g;a.stopPropagation&&a.stopPropagation();a.preventDefault&&a.preventDefault();var b=O("gbmps");if(b){var c=b.style.display=="none";try{var d=O("gbd4"),e=O("gbmps"),f=O("gbmpdv");if(d&&e&&f){f.style.display=c?"none":"";e.style.display=c?"":"none";Ub(d)}}catch(h){C(h,"sp","tav")}}}catch(i){C(i,"sp","tave")}return l};Y.prototype.ra=function(){try{var a=O("gbmpas");a&&Tb(a);this.H=l}catch(b){C(b,"sp","cam")}};
Y.prototype.Oa=function(){var a=O("gbmpdv"),b=O("gbmps");if(a&&b){a.style.display="";b.style.display="none";if(!this.H){var c=O("gbmpal"),d=O("gbpm");if(c){a.style.width="";b.style.width="";c.style.width="";if(d)d.style.width="1px";var e=P(a).width,f=P(b).width;e=e>f?e:f;if(f=O("gbg4")){f=P(f).width;if(f>e)e=f}if(K()){f=Cb();if(f==6||f==7&&document.compatMode=="BackCompat")e+=2}e+="px";a.style.width=e;b.style.width=e;c.style.width=e;if(d)d.style.width=e;this.H=g}}}};
Y.prototype.qa=function(a,b,c,d,e,f,h,i){try{var j=O("gbmpas");if(j){var m="gbmtc";if(a)m+=" gbmpmta";var s=X("div",m),x=X("div","gbmpph");s.appendChild(x);var u=X(f?"a":"span","gbmpl");V(u,"gbmt");if(f){if(i)for(var D in i)u.setAttribute(D,i[D]);u.href=h;W(u,ga(Qb,"gbmt"))}s.appendChild(u);var E=X("span","gbmpmn");u.appendChild(E);E.appendChild(document.createTextNode(d||e));if(a){var Ia=X("span","gbmpmtc");E.appendChild(Ia)}var F=X("span","gbmpme");u.appendChild(F);a=e;if(b)a=this.ua.replace("%1$s",
e);else if(c)a=this.va.replace("%1$s",e);F.appendChild(document.createTextNode(a));j.appendChild(s)}}catch(N){C(N,"sp","aa")}};var Wb=function(a,b){var c=O("gbd4"),d=O("gbmpn");if(c&&d){Tb(d);d.appendChild(document.createTextNode(b));Ub(c)}};Y.prototype.R=function(){try{Xb(this,"gbi4i","gbi4id")}catch(a){C(a,"sp","gbpe")}};Y.prototype.ba=function(){try{Xb(this,"gbmpi","gbmpid")}catch(a){C(a,"sp","ppe")}};var Xb=function(a,b,c){if(a=O(b))a.style.display="none";if(c=O(c))c.style.display=""};
Y.prototype.K=function(){try{if(!this.ga){this.ga=g;var a=O("gbmpi");if(a&&this.F)a.src=this.F}}catch(b){C(b,"sp","spp")}};Y.prototype.Qa=function(a){try{var b=O("gbi4t");(O("gbmpn").firstChild&&O("gbmpn").firstChild.nodeValue?O("gbmpn").firstChild.nodeValue:"")==this.v||Wb(this,a);if((b.firstChild&&b.firstChild.nodeValue?b.firstChild.nodeValue:"")!=this.v){Tb(b);b.appendChild(document.createTextNode(a))}}catch(c){C(c,"sp","spn")}};
Y.prototype.Ra=function(a){try{var b=O("gbmpi");if(b){var c=a(b.height);if(c)this.F=b.src=c}var d=O("gbi4i");if(d){var e=a(d.height);if(e)d.src=e}}catch(f){C(f,"sp","spp")}};Y.prototype.Ta=function(){try{var a=O("gbg4");this.K();zb(k,a,g,g)}catch(b){C(b,"sp","sd")}};H("prf",{init:function(a){new Y(a)}});var Yb=function(){};aa(Yb);var Zb=k;H("il",{init:function(){Yb.D();var a;if(!Zb){a:{a="gbar.logger".split(".");for(var b=o,c;c=a.shift();)if(b[c]!=k)b=b[c];else{a=k;break a}a=b}Zb=a||{}}a=Zb;p(a.il)=="function"&&a.il(8,void 0)}});var cc=function(a,b){if(window.gbar.logger._itl(b))return b;var c=a.stack;if(c){c=c.replace(/\s*$/,"").split("\n");for(var d=[],e=0;e<c.length;e++)d.push($b(c[e]));c=d}else c=ac();d=c;e=0;for(var f=d.length-1,h=0;h<=f;h++)if(d[h]&&d[h].name.indexOf("_mlToken")>=0){e=h+1;break}e==0&&f--;c=[];for(h=e;h<=f;h++)d[h]&&!(d[h].name.indexOf("_onErrorToken")>=0)&&c.push("> "+bc(d[h]));d=[b,"&jsst=",c.join("")];e=d.join("");if(!window.gbar.logger._itl(e))return e;if(c.length>2){d[2]=c[0]+"..."+c[c.length-1];
e=d.join("");if(!window.gbar.logger._itl(e))return e}return b};H("er",{init:function(){window.gbar.logger._aem=cc}});var $b=function(a){var b=a.match(dc);if(b)return new ec(b[1]||"",b[2]||"",b[3]||"","",b[4]||b[5]||"");if(b=a.match(fc))return new ec("",b[1]||"","",b[2]||"",b[3]||"");return k},dc=RegExp("^    at(?: (?:(.*?)\\.)?((?:new )?(?:[a-zA-Z_$][\\w$]*|<anonymous>))(?: \\[as ([a-zA-Z_$][\\w$]*)\\])?)? (?:\\(unknown source\\)|\\(native\\)|\\((?:eval at )?((?:http|https|file)://[^\\s)]+|javascript:.*)\\)|((?:http|https|file)://[^\\s)]+|javascript:.*))$"),fc=/^([a-zA-Z_$][\w$]*)?(\(.*\))?@(?::0|((?:http|https|file):\/\/[^\s)]+|javascript:.*))$/,
ac=function(){for(var a=[],b=arguments.callee.caller,c=0;b&&c<20;){var d;d=(d=Function.prototype.toString.call(b).match(gc))?d[1]:"";var e=b,f=["("];if(e.arguments)for(var h=0;h<e.arguments.length;h++){var i=e.arguments[h];h>0&&f.push(", ");typeof i=="string"?f.push('"',i,'"'):f.push(String(i))}else f.push("unknown");f.push(")");a.push(new ec("",d,"",f.join(""),""));try{if(b==b.caller)break;b=b.caller}catch(j){break}c++}return a},gc=/^function ([a-zA-Z_$][\w$]*)/,ec=function(a,b,c,d,e){this.O=a;this.name=
b;this.L=c;this.Ka=d;this.$=e},bc=function(a){var b=[a.O?a.O+".":"",a.name?a.name:"anonymous",a.Ka,a.L?" [as "+a.L+"]":""];if(a.$){b.push(" at ");b.push(a.$)}a=b.join("");for(b=window.location.href.replace(/#.*/,"");a.indexOf(b)>=0;)a=a.replace(b,"[page]");return a=a.replace(/http.*?extern_js.*?\.js/g,"[xjs]")};var hc=function(a){this.P=a},ic=/\s*;\s*/;hc.prototype.set=function(a,b,c,d,e,f){if(/[;=\s]/.test(a))throw Error('Invalid cookie name "'+a+'"');if(/[;\r\n]/.test(b))throw Error('Invalid cookie value "'+b+'"');c!==undefined||(c=-1);e=e?";domain="+e:"";d=d?";path="+d:"";f=f?";secure":"";c=c<0?"":c==0?";expires="+(new Date(1970,1,1)).toUTCString():";expires="+(new Date(ha()+c*1E3)).toUTCString();this.P.cookie=a+"="+b+e+d+c+f};
hc.prototype.get=function(a,b){for(var c=a+"=",d=(this.P.cookie||"").split(ic),e=0,f;f=d[e];e++)if(f.indexOf(c)==0)return f.substr(c.length);return b};var jc=new hc(document);jc.bb=3950;var Z=window.gbar.i;var lc=function(a){this.B={};this.fb={};Z.g=r(this.Ma,this);Z.h=r(this.La,this);var b=this.B;a=a.p.split(";");for(var c=0,d;d=a[c];++c){d=d.split(",");if(d.length==4){var e={};e.id=d[0];e.ea=d[1];e.eb=Z.c(d[2],0);e.cb=Z.c(d[3],0);b[e.id]=e}}for(var f in this.B){b=this.B[f];if(jc.get("OGH")===undefined){if(a=kc[b.ea])(a=document.getElementById(a))&&B.ca(a,"gbto");B.logger.il(36,{pr:b.id})}}},kc={c:"gbprc"};lc.prototype.Ma=function(a){mc(this,a);B.logger.il(37,{pr:a})};
lc.prototype.La=function(a){mc(this,a);B.logger.il(38,{pr:a})};var mc=function(a,b){var c=a.B[b];if(c){if(c=kc[c.ea])if(c=document.getElementById(c)){B.cr(c,"gbto");c.style.display="none"}jc.set("OGH","1",1209600,"/",".google.com")}};H("pm",{init:function(a){new lc(a)}});var nc=function(){this.U=l};aa(nc);var oc=["gb","gbpr","gbx3","gbx4","gbq","gbu","gbx1","gbx2","gbbw","gbpra"];nc.prototype.G=function(a){this.Aa=a.he;this.za=a.ha;this.Ya=a.ad};nc.prototype.ta=function(){pc(this,l);B.elh&&B.elh(this.za);Z.f&&Z.f();B.elx&&B.elx()};var pc=function(a,b){for(var c=0,d;d=oc[c];c++)if(d=O(d))b?V(d,"gbprat"):Q(d,"gbprat")};H("prb",{init:function(a){nc.D().G(a)}});var $=function(){var a=O("gbqlw");if(a)a.onclick=k;if(B.gpoas){t("gbar.gpoas",r(this.Y,this));t("gbar.gpcas",r(this.sa,this))}this.Y();a=O("gbq1");var b=O("gbqlw");if(b){W(b,r(this.Fa,this));M(b,"keydown",r(this.Va,this))}(b=O("gbpr"))&&W(b,r(this.Ha,this));b=O("gbztm");var c=O("gbtem");if(b&&c){M(b,"keydown",r(this.N,this));M(c,"keydown",r(this.N,this))}try{var d=O("gbqlw");d&&M(d,"click",r(this.ja,this))}catch(e){C(e,"as","east")}d=O("gbztm");b=O("gbd");if(d){W(d,r(this.Z,this),"mouseover");M(d,
"click",r(this.Wa,this))}b&&M(b,"click",r(Nb,this,"gbd"));a&&W(a,r(this.Ca,this));if(a=O("gbz")){d=r(this.Sa,this,window.location.hostname);M(a,"mouseover",d)}if(document.body.style.MozTransform!=undefined&&document.body.style.MozTransition==undefined)this.k=l;else if(K())this.k=l;if(d=O("gbm1")){b=ib(O("gbzc")).length-1;a=[];c=ib(d);for(var f=b,h;h=c[f];++f)a.push(h);c.length<b&&qc(this,d,b-c.length);d=ib(O("gbzc")).length-1;b=O("gbtem");c=O("gbdi");f=1;for(var i=O("gbm"+f);h=a.shift();){for(var j=
k;i&&!(j=rc(this,i));){f++;i=O("gbm"+f)}if(!i){i=d;j=X("div","gbmasc");qc(this,j,i);i=j;i.id="gbm"+f;c.insertBefore(i,b);j=rc(this,i)}i.replaceChild(h,j)}}this.j=undefined;B.ach("gbz",r(this.Ea,this));B.aeh("gbz",g)};n=$.prototype;n.w=g;n.V=l;n.a=0;n.u=0;n.n=0;n.t=0;n.r=0;n.o=0;n.b=0;n.k=g;n.S=l;n.T=l;n.X=l;n.A=undefined;n.Y=function(){var a=O("gbq1");if(a&&S(a,"gbtoc")){this.X=g;this.I("click")}};n.sa=function(){R(k);sc(this)};
n.Va=function(a){try{var b=a.target||a.srcElement;if(a.keyCode&&b)if(a.keyCode==13||a.keyCode==3)this.ja(a)}catch(c){C(c,"as","tke")}};n.ja=function(a){try{Jb(a);if(this.a&&this.n){clearTimeout(this.n);this.n=0;this.z(2)}else if(this.a){sc(this);B.logger.il(30)}else{this.I(a.type);B.logger.il(29)}}catch(b){C(b,"as","tas")}};
n.I=function(a){try{var b=a=="keydown";if(!this.a){var c=O("gbqlw"),d=O("gbz"),e=O("gbqla"),f=O("gbq1");if(d&&c&&e&&f){var h=d.style;zb(k,c,g,!b);if(b){var i=d.getElementsByTagName("a");i&&i.length&&i[0].focus&&i[0].focus()}tc(this);uc(this,g);yc(this,d,h,e);if(a=="click"){this.z(2);this.n=0}else{this.z(1);this.n=setTimeout(r(this.Ga,this),500)}zc(this)}}}catch(j){C(j,"as","oasi")}};n.Ga=function(){this.n=0};n.Da=function(){if(this.a==1&&this.b!=2)sc(this);else this.b!=2&&Ac(this)};
var sc=function(a){try{if(a.a){Ac(a);Bc(a,g);tc(a);uc(a);Ac(a,0);var b=O("gbz"),c=O("gbqla");if(b&&c){P(b);var d=b.style,e=c.style;V(b,"gbzat");d.overflow="hidden";V(c,"gbqlat");d.opacity="0";if(a.k)e.opacity="0";var f=a.k?218:0;a.r=Vb(r(a.da,a,b,d,c),f)}a.z(0);zc(a);if(a.T){var h=nc.D();if(h.Aa&&!h.U){h.U=g;var i=O("gb");if(i){pc(h,g);Q(i,"gbpro");if(K()){var j=O("gbpra");if(j){j.style.visibility="hidden";for(var m=j.firstChild;m;m=m.nextSibling)m.style.visibility="hidden"}}window.setTimeout(r(h.ta,
h),h.Ya);B.logger.il(33)}}}}}catch(s){C(s,"as","cawi")}};$.prototype.N=function(a){try{var b=a||window.event,c=(b.target||b.srcElement).id,d=b.shiftKey;if(b.keyCode==9&&!d)if(c=="gbztm")this.b||sc(this);else{sc(this);var e=document.getElementById("gbqfqwb");e&&e.focus()}}catch(f){C(f,"as","caob")}};$.prototype.Ca=function(a){try{Cc(this,a);if(this.w)try{if(this.a&&!this.t){var b=this.a==1?400:400;this.t=window.setTimeout(r(this.Da,this),b)}}catch(c){C(c,"as","casd")}}catch(d){C(d,"as","oamhe")}};
$.prototype.Fa=function(a){try{Cc(this,a);if(!this.w)try{if(!this.a&&!this.u){var b;var c=O("gbqlw");if(!c||!c.clientHeight)b=500;else{var d=P(c).height,e=300;if(a&&a.type=="mouseover"&&a.clientY!==undefined){var f;if(a.pageY!==undefined)f=a.pageY;else{var h=!Oa&&document.compatMode=="CSS1Compat"?document.documentElement:document.body,i=document.parentWindow||document.defaultView;f=a.clientY+(new xa(i.pageXOffset||h.scrollLeft,i.pageYOffset||h.scrollTop)).y}for(;c;){f-=c.offsetTop;c=c.offsetParent}if(f<
d/2)e=45}b=Math.min(500,1E3*d/e)}this.u=window.setTimeout(r(this.I,this,a.type),b);B.logger.il(28)}}catch(j){C(j,"as","oasad")}}catch(m){C(m,"as","olhe")}};var Cc=function(a,b){var c;if(b.type=="mouseover")c=l;else{c=b||window.event;var d=c.type,e=Rb(c),f=O("gbq1");if(d=="click")e=c.target||b.srcElement;c=Sb(f,e)?g:l;c=!c}a.w=c;if(a.w){clearTimeout(a.u);a.u=0}else{clearTimeout(a.t);a.t=0}zc(a)};$.prototype.Ha=function(a){try{this.V=a.type=="mouseover";zc(this)}catch(b){C(b,"as","opbhe")}};
var yc=function(a,b,c,d){c.overflow="visible";c.opacity="1";Q(b,"gbzat");d.style.opacity="1";Q(d,"gbqlat");a.r=0};$.prototype.da=function(a,b,c){R();Q(a,"gbzat");b.height="auto";b.overflow="visible";Q(c,"gbqlat");this.r=0};
var tc=function(a){clearTimeout(a.u);a.u=0;clearTimeout(a.n);a.n=0;clearTimeout(a.t);a.t=0},uc=function(a,b){Bc(a,b);if(a.r){clearTimeout(a.r);a.r=0;if(b){var c=O("gbz"),d=O("gbqla");if(c&&d)a.a?yc(a,c,c.style,d):a.da(c,c.style,d)}}},Bc=function(a,b){if(a.o){clearTimeout(a.o);a.o=0;b&&a.J()}},zc=function(a){try{var b=O("gbx1"),c=O("gbx2");if(b&&c)if(!a.w||a.V){V(b,"gbxngh");V(c,"gbxngh")}else{Q(b,"gbxngh");Q(c,"gbxngh")}}catch(d){C(d,"as","sbhs")}};
$.prototype.Wa=function(a){try{Jb(a);if(this.o)this.b&&Dc(this,2);else this.b?Ac(this):this.Z(a)}catch(b){C(b,"as","tmm")}};
$.prototype.Z=function(a){try{var b=O("gbz"),c=O("gbd");if(b&&c&&!this.b){Bc(this,g);var d=c.style,e=P(b).height-2,f=P(c).width;b={};b.height=e;b.width=f;this.k&&V(c,"gbdat");d.height=b.height+"px";d.width=b.width+"px";d.visibility="visible";d.overflow="hidden";Dc(this,a.type=="click"?2:1);var h=this.k?400:0;this.o=Vb(r(this.J,this),h);if(B.gpcc&&B.gpcc()){var i=document.activeElement;if(i&&i.name=="q"){i.blur();this.A=i}}}}catch(j){C(j,"as","omm")}};
var Ac=function(a,b){var c=O("gbd");if(c&&a.b){Bc(a,g);var d=c.style,e=a.k?b!==undefined?b:400:0;a.k&&V(c,"gbdat");d.width="auto";d.overflow="hidden";Dc(a,0);a.o=Vb(r(a.J,a),e);if(a.A){a.A.focus();a.A=undefined}}};
$.prototype.J=function(){var a=O("gbz"),b=O("gbd");if(a&&b){var c=b.style;c.visibility=this.b?"visible":"hidden";c.overflow="";Q(b,"gbdat");if(this.b){a=P(a).width;b=P(b).width;if(c=O("gbs")){c=c.style;var d="right";if(Hb)d="left";var e=c[d];this.j={};this.j.cssEndEdge=d;this.j.cssEndEdgeValue=e;this.j.cssWidth=a+"px";c.width=a+b+"px";if(e.substr(-2)=="px")c[d]=parseInt(e,10)-b+"px"}}else if((a=O("gbs"))&&this.j){a=a.style;b=this.j.cssEndEdge;c=this.j.cssEndEdgeValue;a.width=this.j.cssWidth;a[b]=
c}}this.o=0};$.prototype.Sa=function(a){try{if(!this.X&&!this.S){this.S=g;var b=a.indexOf(".google");if(b>0){jc.set("OGP","",604800,"/",a.substring(b));B.logger.il(32);this.T=g}}}catch(c){C(c,"as","spbc")}};var rc=function(a,b){for(var c=ib(b),d=0,e;e=c[d];++d)if(S(e,"gbmasph"))return e;return k},qc=function(a,b,c){for(a=0;a<c;++a){var d=X("span","gbmasph");b.appendChild(d)}};
$.prototype.Ea=function(){var a=document.activeElement;if(a){var b=O("gbz"),c=O("gbd");if(b&&c)if(Sb(b,a)||Sb(c,a))a.blur()}Ac(this);window.setTimeout(r(this.z,this,0),50)};$.prototype.z=function(a){this.a=a;Ec(this,"gbzb",a)};var Dc=function(a,b){a.b=b;Ec(a,"gbmb",a.a)},Ec=function(a,b,c){if(a=O(b))a.style.visibility=c==1?"visible":"hidden"};H("as",{init:function(a){new $(a)}});var Fc=function(){this.W=l;if(!this.W){M(window,"resize",r(this.Ja,this),g);this.W=g}};Fc.prototype.C=0;Fc.prototype.Ia=function(){B.elg();this.C=0};Fc.prototype.Ja=function(){B.elg();this.C&&window.clearTimeout(this.C);this.C=window.setTimeout(r(this.Ia,this),1500)};H("el",{init:function(a){new Fc(a)}});var Gc=function(){this.Q=l;this.G()};n=Gc.prototype;n.G=function(){var a=document.getElementById("gbqfq"),b=document.getElementById("gbqfqwb");if(a&&b&&!this.Q){M(a,"focus",r(this.fa,this));M(a,"blur",r(this.Ua,this));M(b,"click",r(this.Pa,this));this.Q=g}document.activeElement==document.getElementById("gbqfq")&&this.fa();t("gbar.qfhi",r(this.Za,this))};n.fa=function(){try{var a=document.getElementById("gbqfqw");a&&V(a,"gbqfqwf")}catch(b){C(b,"sf","stf")}};
n.Ua=function(){try{var a=document.getElementById("gbqfqw");a&&Q(a,"gbqfqwf")}catch(b){C(b,"sf","stb")}};n.Pa=function(){try{var a=document.getElementById("gbqfq");a&&a.focus()}catch(b){C(b,"sf","sf")}};n.Za=function(a){var b=document.getElementById("gbqffd");if(b){b.innerHTML="";if(a)for(var c in a){var d=document.createElement("input");d.name=c;d.value=a[c];d.type="hidden";b.appendChild(d)}}};H("sf",{init:function(a){new Gc(a)}});t("gbar.bbs",function(a){try{for(var b=a[0],c=[],d=1;d<=3;d++){var e,f=/^(.*?)\$(\d)\$(.*)$/.exec(b);e=f?{index:parseInt(f[2],10),aa:f[1],Na:f[3]}:k;if(!e)break;if(e.index>3)throw Error();e.aa&&c.push(e.aa);c.push(gb("A",{href:"#gbbb"+e.index},a[e.index]));b=e.Na}b&&c.push(b);for(var h=document.getElementById("gbbbc"),i;i=h.firstChild;)h.removeChild(i);hb(h,c);var j=document.getElementById("gbbbb").style;j.opacity="0";j.filter="alpha(opacity=0)";j.WebkitTransform=j.MozTransform=j.OTransform=j.transform=
"scale(.2)";j.WebkitTransition=j.MozTransition=j.OTransition=j.Xa="all 0.218s";j.opacity="1";j.filter="alpha(opacity=100)";j.WebkitTransform=j.MozTransform=j.OTransform=j.transform="scale(1)"}catch(m){C(m,"bb","s")}});
t("gbar.bbh",function(){var a=document.getElementById("gbbbb").style;a.WebkitTransition="opacity 1s, -webkit-transform 0 linear 1s";a.MozTransition="opacity 1s, -moz-transform 0s linear 1s";a.OTransition="opacity 1s, -o-transform 0 linear 1s";a.Xa="opacity 1s, transform 0 linear 1s";a.opacity="0";a.filter="alpha(opacity=0)";a.WebkitTransform=a.MozTransform=a.OTransform=a.transform="scale(.2)"});I(G.la);
(function(){I(G.na);var a,b;for(a=0;b=B.bnc[a];++a)if(b[0]=="m")break;if(b&&!b[1].l){a=function(){for(var c=B.mdc,d=B.mdi||{},e=0,f;f=kb[e];++e){var h=f[0],i=c[h],j=d[h],m;if(m=i){if(j=!j){var s;a:{j=h;if(m=B.mdd)try{if(!lb){lb={};var x=m.split(/;/);for(m=0;m<x.length;++m)lb[x[m]]=g}s=lb[j];break a}catch(u){B.logger&&B.logger.ml(u)}s=l}j=!s}m=j}if(m){I(G.pa,h);try{f[1].init(i);d[h]=g}catch(D){B.logger&&B.logger.ml(D)}I(G.oa,h)}}if(c=B.qd.m){B.qd.m=[];for(d=0;e=c[d];++d)try{e()}catch(E){B.logger&&B.logger.ml(E)}}b[1].l=
g;I(G.ma);a:{for(c=0;d=B.bnc[c];++c)if((d[1].auto||d[0]=="m")&&!d[1].l){c=l;break a}c=g}c&&I(G.ka)};if(!b[1].libs||B.agl&&B.agl(b[1].libs))a();else b[1].i=a}})();}catch(e){window.gbar&&gbar.logger&&gbar.logger.ml(e,{"_sn":"m.init"});}})();