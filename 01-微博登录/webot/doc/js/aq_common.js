!
function() {
	var t, e, l = ["https://aq.qq.com/cn2/manage/mbtoken/hijack_sec_js_report", "https://zyjc.sec.qq.com/dom", "https://aq.qq.com/cn2/manage/mbtoken/hijack_pv_report", "https://aq.qq.com/cn2/manage/mbtoken/hijack_xss_report", "https://aq.qq.com/cn2/manage/mbtoken/hijack_mv_js_report"],
		a = Math.random(),
		c = .01,
		d = !1;

	function f(t, e) {
		for (var n = new Array, o = 0; o < t.length; o++) if ("&" == t.charAt(o)) {
			var r = [3, 4, 5, 9],
				a = 0;
			for (var c in r) {
				var i = r[c];
				if (o + i <= t.length) {
					var m = t.substr(o, i).toLowerCase();
					if (e[m]) {
						n.push(e[m]), o = o + i - 1, a = 1;
						break
					}
				}
			}
			0 == a && n.push(t.charAt(o))
		} else n.push(t.charAt(o));
		return n.join("")
	}

	function g(t) {
		return document.createElement(t)
	}

	function q(t) {
		t && t.parentNode && t.parentNode.removeChild(t)
	}

	function h(t) {
		var e, n, o, r, a, c, i, m, p, u = t.url,
			d = t.data,
			h = "aq_form" + 1e17 * Math.random(),
			s = (e = u, n = h, o = "post", (r = g("form")).action = e, r.method = o, r.target = n, r.style.display = "none", r),
			l = (a = h, (c = g("iframe")).name = a, c.src = "javascript:void(0);", c.style.display = "none", c);
		for (var f in document.body.appendChild(l), l.contentWindow.name = h, d) s.appendChild((m = d[i = f], p = void 0, (p = g("input")).name = i, p.value = m, p));
		document.body.appendChild(s), s && s.submit(), setTimeout(function() {
			q(s), q(l)
		}, 2e3)
	}

	function v(t) {
		(new Image).src = t
	}!
	function() {
		for (var t = new Object, e = "'\"<>`script:daex/hml;bs64,", n = 0; n < e.length; n++) {
			for (var o = e.charAt(n), r = o.charCodeAt(), a = r, c = r.toString(16), i = 0; i < 7 - r.toString().length; i++) a = "0" + a;
			t["&#" + r + ";"] = o, t["&#" + a] = o, t["&#x" + c] = o
		}
		t["&lt"] = "<", t["&gt"] = ">", t["&quot"] = '"';
		var m = location.href,
			p = document.referrer;
		m = decodeURIComponent(f(m, t)), p = decodeURIComponent(f(p, t));
		var u = new RegExp("['\"<>`]|script:|data:text/html;base64,");
		if (u.test(m) || u.test(p)) {
			var d = l[1],
				h = new Image;
			Math.random() < .1 && v(l[3] + "?v=2&u=" + encodeURIComponent(m) + "&r=" + encodeURIComponent(p)), h.src = d + "?v=2&u=" + encodeURIComponent(m) + "&r=" + encodeURIComponent(p), s = location.host, (/(\.|^)(wegame|tgp\.qq)\.com$/i.test(s) || /(\.|^)we\.game$/i.test(s)) && !/(\.|^)developer\.wegame\.com$/i.test(s) || (m = (m = m.replace(/['\"<>`]|script:/gi, "M")).replace(/data:text\/html;base64,/gi, "data:text/plain;base64,"), location.href = encodeURI(m))
		}
		var s
	}(), function(i, m, p) {
		function t(t, e, n) {
			var o, r, a, c = {
				bid: e,
				childUrl: "",
				parentUrl: ""
			};
			try {
				c.childUrl = p.href
			} catch (t) {}
			try {
				c.parentUrl = parent.location.href
			} catch (t) {}
			if (1 == n) try {
				parent != i && u(parent.document, "datapp", c)
			} catch (t) {} else {
				try {
					u(m, "datapt", c), parent != i && (o = parent.document, r = "datapp", void(x((a = c).parentUrl) && u(o, r, a)))
				} catch (t) {}
				try {
					parent != i &&
					function(t) {
						if (x(t.parentUrl)) {
							var e = [];
							e.push("beframed::url"), b(e, "beframed", t)
						}
					}(c)
				} catch (t) {}
			}
		}

		function b(t, e, n) {
			var o;
			l[0], new Image;
			if (t.push("childUrl::" + encodeURIComponent(n.childUrl)), t.push("parentUrl::" + encodeURIComponent(n.parentUrl)), !d && a < c && (o = t.join("|"), v(l[2] + "?host=" + encodeURIComponent(location.host) + "&data=" + o + "&hp=1&tk=" + +new Date), d = !0), Math.random() < .9) return !1;
			var r = {
				id: n.bid,
				imark: e,
				data: t.join("|")
			};
			return Math.random() < 1 && (r.dom = encodeURIComponent(document.documentElement.outerHTML), r.plgs = encodeURIComponent(function() {
				var t = navigator.plugins,
					e = "";
				if (t && t.length) {
					e = [];
					for (var n = 0; n < t.length; n++) {
						var o = t[n].name,
							r = t[n].description;
						e.push(o + "::" + r)
					}
					e = e.join(";")
				}
				return e
			}())), h({
				data: r,
				url: l[0]
			}), !0
		}

		function w(t, e, n) {
			try {
				var o = location.host;
				if ("m.v.qq.com" != o && "v.qq.com" != o && retrun, .1 < Math.random()) return !1;
				!
				function(t, e, n) {
					try {
						var o = l[4],
							r = new Image;
						t.push("childUrl::" + encodeURIComponent(n.childUrl)), t.push("parentUrl::" + encodeURIComponent(n.parentUrl)), r.src = o + "?id=" + n.bid + "&imark=" + e + "&data=" + t.join("|") + "&random=" + Math.random()
					} catch (t) {}
				}([], e, n)
			} catch (t) {}
		}

		function u(t, e, n) {
			w(0, e, n);
			var o, r, a, c, i, m, p, u, d = function(t) {
					for (var e, n, o, r, a = t.getElementsByTagName("script"), c = [], i = 0; i < a.length; i++) e = a[i], (n = e.src) && c.push(n);
					return o = U(c, x), r = C("script"), I(o, r)
				}(t),
				h = (o = t, r = C("iframe"), j(o, "IFRAME", function(t) {
					return t.src
				}, x, r)),
				s = (a = t, c = C("frame"), j(a, "FRAME", function(t) {
					return t.src
				}, x, c)),
				l = (i = t, m = C("embed"), j(i, "EMBED", function(t) {
					return t.src
				}, x, m)),
				f = (p = t, u = C("img"), j(p, "IMG", function(t) {
					return t.src
				}, x, u)),
				g = function(t) {
					for (var e, n, o, r, a = t.getElementsByTagName("source"), c = [], i = 0; i < a.length; i++) e = a[i], (n = e.src) && c.push(n);
					return o = U(c, x), r = C("source"), I(o, r)
				}(t),
				q = function(t) {
					for (var e, n, o, r, a = t.getElementsByTagName("video"), c = [], i = 0; i < a.length; i++) e = a[i], (n = e.src) && c.push(n);
					return o = U(c, x), r = C("video"), I(o, r)
				}(t),
				v = function(t) {
					for (var e, n, o, r, a = t.getElementsByTagName("object"), c = [], i = 0; i < a.length; i++) e = a[i], (n = e.data) && c.push(n);
					return o = U(c, x), r = C("object"), I(o, r)
				}(t),
				y = d.concat(h, s, f, l, g, q, v);
			if (y.length <= 0) return !1;
			b(y = function(t) {
				var e = t.slice(0),
					n = [];
				e.sort(), n.push(e[0]);
				for (var o = 1; o < e.length; o += 1) e[o] != e[o - 1] && n.push(e[o]);
				return n
			}(y), e, n)
		}

		function U(t, e) {
			for (var n = [], o = 0; o < t.length; ++o) {
				var r = t[o];
				e(r) && n.push(r)
			}
			return n
		}

		function x(t) {
			var e, n, o, r, a = function(t) {
					var e = /^https?:\/\/([\w\-]+\.[\w\-.]+)/i.exec(t);
					if (!e) return;
					return e[1]
				}(t);
			return !!a && (e = /(\.|^)(qq|paipai|soso|wenwen|tenpay|macromedia|gtimg|qstatic|qqmail|paipaiimg|qqgames|pengyou|foxmail|qzoneapp|qzone|qplus|imqq|tqapp|tencent|3366|21mmo|taotao|imrworldwide|idqqimg|17roco|expo2010china|fangqq|tencentmind|tencity|yingkebicheng|zhangzhongxing|expovol|otaworld|gzyunxun|heyyo|himoral|himorale|myrtx|qqwinner|redian|sjkx|rtxonline|nbaso|paipai\.500wan|qqjapan|qq\.salewell|sogou|weiyun|flzhan|wechat|webplat\.ied|qcloud)\.com$/i, n = /(\.|^)(qq\.com|gtimg|gtimg\.com|qlogo|foxmail\.com|gtimg\.com|url|qpic|tencent\.com|expo2010|expo|himorale\.com|nbaso\.com|qqtest\.com|qq\.ucar|rtx\.com|soso\.com|tcimage|taoche)\.cn$/i, o = /(\.|^)(5999|gongyi)\.net$/i, r = /(\.|^)(himorale\.com\.hk|tencent\.com\.hk|qq\.chinacache\.net|qq\.com\.fastcdn\.com|qq\.com\.lxdns\.com|qq\.fastcdn\.com|soso\.com\.lxdns\.com|motu\.pagechoice\.net|ope\.tanx\.com|dap\.gentags\.net|widget\.weibo\.com)$/i, !(/^xui.ptlogin2?\.?$/i.test(a) || e.test(a) || n.test(a) || o.test(a) || r.test(a)))
		}

		function C(e) {
			return function(t) {
				return e + "::" + encodeURIComponent(t)
			}
		}

		function I(t, e) {
			for (var n, o = [], r = 0; r < t.length; ++r) n = e(t[r]), o.push(n);
			return o
		}

		function j(t, e, n, o, r) {
			return I(U(I(t.getElementsByTagName(e), n), o), r)
		}
		try {
			setTimeout(function() {
				t(0, 100, 0), function(t) {
					function e(t) {
						var e = document.createElement("script");
						e.src = "https://captcha.gtimg.com/public/2/web-token.0.0.1.js", e.defer = !0, e.onerror = t ||
						function() {}, document.body ? document.body.appendChild(e) : document.head.appendChild(e)
					}
					try {
						var n = location.host;
						if ("zj.qq.com" != n && "sh.qq.com" != n && "hb.qq.com" != n && "henan.qq.com" != n && retrun, Math.random() > t) return;
						e(function() {
							e()
						})
					} catch (t) {}
				}(1)
			}, 5e3)
		} catch (t) {}
	}(window, document, location), a < c && (t = location.protocol, e = "", e = 0 <= t.indexOf("https") || 0 <= t.indexOf("HTTPS") ? "https" : 0 <= t.indexOf("http") || 0 <= t.indexOf("HTTP") ? "http" : t, v(l[2] + "?host=" + encodeURIComponent(location.host) + "&p=" + encodeURIComponent(e) + "&hp=0&tk=" + +new Date))
}();