const { reportKeyMap } = require('../../../data/reportKeys');

module.exports = (req, res) => {
    const slug = req.query.slug || '';
    const uniqueKey = slug.slice(-12).toUpperCase();
    const report = reportKeyMap[uniqueKey];

    if (!report) {
        res.writeHead(302, { Location: '/' });
        res.end();
        return;
    }

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report #${report.taskNumber} | Janoshik Analytical</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.65; color: #585858; background: #fff; -webkit-font-smoothing: antialiased; }
        a { color: #3ba666; text-decoration: none; transition: color 0.2s ease; }
        a:hover { color: #2d7d4e; }
        img { max-width: 100%; height: auto; }
        ul { list-style: none; }
        #header { background: #2a2a2a; color: #fff; padding: 0 2em; display: flex; align-items: center; justify-content: space-between; height: 3.5em; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }
        #header h1 { font-size: 1.25em; font-weight: 600; letter-spacing: 0.05em; }
        #header h1 a { color: #fff; }
        #header h1 a:hover { color: #3ba666; }
        #header nav ul { display: flex; gap: 1.5em; }
        #header nav ul li a { color: rgba(255,255,255,0.75); font-size: 0.9em; font-weight: 400; text-transform: uppercase; letter-spacing: 0.1em; padding: 0.5em 0; }
        #header nav ul li a:hover { color: #fff; }
        .navToggle { display: none; width: 2.5em; height: 2.5em; position: relative; cursor: pointer; }
        .navToggle .hamburger { display: block; width: 1.5em; height: 2px; background: #fff; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
        .navToggle .hamburger::before, .navToggle .hamburger::after { content: ''; display: block; width: 1.5em; height: 2px; background: #fff; position: absolute; left: 0; }
        .navToggle .hamburger::before { top: -6px; }
        .navToggle .hamburger::after { top: 6px; }
        #navPanel { position: fixed; top: 0; left: 0; width: 280px; height: 100%; background: #2a2a2a; z-index: 2000; transform: translateX(-100%); transition: transform 0.3s ease; padding: 3em 1.5em 1.5em; overflow-y: auto; }
        #navPanel.visible { transform: translateX(0); }
        #navPanel nav a { display: block; color: rgba(255,255,255,0.75); font-size: 1em; padding: 0.75em 0; border-bottom: 1px solid rgba(255,255,255,0.1); text-transform: uppercase; letter-spacing: 0.1em; }
        #navPanel nav a:hover { color: #fff; }
        #navPanel .close { position: absolute; top: 0.5em; right: 0.75em; font-size: 1.75em; color: rgba(255,255,255,0.5); cursor: pointer; line-height: 1; }
        #navPanel .close:hover { color: #fff; }
        #navPanelOverlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1500; }
        #navPanelOverlay.visible { display: block; }
        #main { padding: 5em 0 3em; }
        .container { max-width: 960px; margin: 0 auto; padding: 0 2em; }
        .image.fit { display: block; }
        .image.fit img { display: block; width: 100%; height: auto; border: medium double rgba(144,144,144,0.25); transition: opacity 0.2s ease; }
        .image.fit img:hover { opacity: 0.9; }
        #footer { background: #2a2a2a; color: rgba(255,255,255,0.5); padding: 2em 0; text-align: center; font-size: 0.85em; }
        @media screen and (max-width: 768px) { #header nav { display: none; } .navToggle { display: block; } #header { padding: 0 1em; } #header h1 { font-size: 1.1em; } .container { padding: 0 1em; } #main { padding: 4.5em 0 2em; } }
    </style>
</head>
<body>
    <header id="header">
        <h1><a href="https://janoshik.com">Janoshik Analytical</a></h1>
        <nav id="nav"><ul><li><a href="https://janoshik.com/">Home</a></li><li><a href="https://janoshik.com/public-results">Public</a></li></ul></nav>
        <a href="#navPanel" class="navToggle" id="navToggle"><span class="hamburger"></span></a>
    </header>
    <div id="navPanel"><nav><a href="https://janoshik.com/" class="link">Home</a><a href="https://janoshik.com/public-results" class="link">Public</a></nav><a href="#" class="close" id="navPanelClose">&times;</a></div>
    <div id="navPanelOverlay"></div>
    <section id="main" class="wrapper"><div class="container"><ul class="alt"><li>
        <a download="Test Report #${report.taskNumber}" href="/reports/${report.dir ? report.dir + '/' + report.filename : report.filename}">
            <span class="image fit"><img src="/reports/${report.dir ? report.dir + '/' + report.filename : report.filename}" alt="Test Report #${report.taskNumber}" title="Click to download" style="border: medium double rgba(144,144,144,0.25)"></span>
        </a>
    </li></ul></div></section>
    <footer id="footer"><div class="container"><p>&copy; Janoshik Analytical. All rights reserved.</p></div></footer>
    <script>
        (function(){var t=document.getElementById('navToggle'),p=document.getElementById('navPanel'),o=document.getElementById('navPanelOverlay'),c=document.getElementById('navPanelClose');function on(){p.classList.add('visible');o.classList.add('visible');document.body.classList.add('navPanel-visible');}function off(){p.classList.remove('visible');o.classList.remove('visible');document.body.classList.remove('navPanel-visible');}t.addEventListener('click',function(e){e.preventDefault();on();});c.addEventListener('click',function(e){e.preventDefault();off();});o.addEventListener('click',off);})();
    </script>
</body>
</html>`;

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end(html);
};
