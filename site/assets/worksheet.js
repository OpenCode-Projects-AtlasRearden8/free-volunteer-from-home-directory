/* Worksheet scoring — runs entirely in your browser. No network requests,
   no storage, no tracking. */
(function () {
  "use strict";

  var ENTRIES = [
    {
      id: "citizen-science",
      name: "Citizen science",
      href: "citizen-science.html",
      score: function (a) {
        var s = 0;
        if (a.time === "tiny") s += 3;
        if (a.people === "no") s += 3;
        if (a.mode === "head") s += 2;
        if (a.mode === "fixing") s += 1;
        if (a.adult === "teen") s += 1;
        return s;
      },
      why: "Five-minute tasks, no talking, and it all counts for real research."
    },
    {
      id: "archive-transcription",
      name: "Archive transcription",
      href: "archive-transcription.html",
      score: function (a) {
        var s = 0;
        if (a.time === "tiny") s += 2;
        if (a.time === "hour") s += 3;
        if (a.people === "no") s += 3;
        if (a.mode === "head") s += 3;
        return s;
      },
      why: "Quiet, focused typing of old documents — short sessions welcome."
    },
    {
      id: "craft-drives",
      name: "Craft drives",
      href: "craft-drives.html",
      score: function (a) {
        var s = 0;
        if (a.mode === "hands") s += 4;
        if (a.people === "no") s += 2;
        if (a.time === "hour") s += 1;
        return s;
      },
      why: "Make one hat or square in front of a show and mail it in."
    },
    {
      id: "accessibility-testing",
      name: "Accessibility testing",
      href: "accessibility-testing.html",
      score: function (a) {
        var s = 0;
        if (a.mode === "fixing") s += 4;
        if (a.people === "typing" || a.people === "voice") s += 1;
        if (a.time === "hour") s += 2;
        return s;
      },
      why: "You already click around websites — now report what breaks."
    },
    {
      id: "online-tutoring",
      name: "Online tutoring",
      href: "online-tutoring.html",
      score: function (a) {
        var s = 0;
        if (a.time === "hour") s += 2;
        if (a.people === "voice") s += 4;
        if (a.people === "typing") s += 2;
        if (a.adult === "adult") s += 2;
        return s;
      },
      why: "One 30-minute session can unstick a student for the whole year."
    },
    {
      id: "remote-crisis-line",
      name: "Remote crisis-line volunteering",
      href: "remote-crisis-line.html",
      score: function (a) {
        var s = 0;
        if (a.time === "committed") s += 4;
        if (a.adult === "adult") s += 3;
        if (a.people === "typing") s += 3;
        if (a.people === "voice") s += 1;
        return s;
      },
      why: "Deep, meaningful support work for people ready to train and show up weekly."
    }
  ];

  function adopt() {
    var g = function (n) {
      var el = document.querySelector('input[name="' + n + '"]:checked');
      return el ? el.value : "";
    };
    return {
      time: g("time"),
      people: g("people"),
      mode: g("mode"),
      adult: g("adult")
    };
  }

  function run() {
    var a = adopt();
    var ranked = ENTRIES.map(function (e) {
      return { entry: e, points: e.score(a) };
    }).sort(function (x, y) { return y.points - x.points; });

    var box = document.getElementById("ws-result");
    if (!box) return;
    var top = ranked[0];
    if (top.entry.id === "remote-crisis-line" && a.time !== "committed") {
      top = ranked[1];
    }
    var html = '<p class="ws-match">Suggested first project: <a href="' +
      top.entry.href + '"><strong>' + top.entry.name +
      "</strong></a></p><p>" + top.entry.why + "</p>";

    var second = ranked.filter(function (r) {
      return r.entry.id !== top.entry.id;
    })[0];
    html += '<p class="ws-runner">Second place worth a look: <a href="' +
      second.entry.href + '">' + second.entry.name + "</a></p>";

    html += "<p>Your first week:</p><ul><li>Read the page for " +
      top.entry.name + " end to end (5 minutes).</li>" +
      "<li>Do the signup steps, or the first tutorial step if there is " +
      "one (20–30 minutes).</li>" +
      "<li>Do the task exactly once. One page, one classification, one " +
      "item, one session.</li>" +
      "<li>Notice how it felt. That is the whole test.</li></ul>";

    box.innerHTML = html;
    box.hidden = false;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("ws-run");
    if (btn) {
      btn.addEventListener("click", run);
    }
  });
})();
