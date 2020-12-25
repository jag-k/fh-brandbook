var through = require('through2');
var fs = require('fs-extra');
var {JSDOM} = require("jsdom");

var reg = /\{\{ icon[s]?\(['"]([-a-z]+)["']/g
var headline = '<?xml version="1.0" encoding="UTF-8"?>';

module.exports.build = (svgPath, svgOut, icons) => () => {
  fs.readFile(svgPath, "utf-8", (err, _data) => {
    var dom = new JSDOM(_data, {
      contentType: "image/svg+xml",
      // runScripts: "dangerously",
    });
    var newDom = new JSDOM(_data, {
      contentType: "image/svg+xml",
      // runScripts: "dangerously",
    });
    var document = dom.window.document.firstChild;
    var doc = newDom.window.document.firstChild;
    doc.innerHTML = '';

    for (var i in icons) {
      var symbol = document.getElementById(i);
      if (symbol === null) console.error('Icon "' + i + '" does not exist!');
      else doc.appendChild(symbol);
    }

    fs.outputFile(svgOut, headline + newDom.serialize().replace(/\n */g, ''), function (err) {
      if (err) {
        console.error(err);
        // throw err
      }
      console.log('The file has been saved!');
    });
  })
};

module.exports.count = (icons) => through.obj((chunk, enc, cb) => {
  fs.readFile(chunk.path, "utf-8", (err, _data) => {
    var arr = [..._data.matchAll(reg)].map((v) => v[1])
    for (var i in arr) {
      icons[arr[i]] = true;
    }
  })
  cb(null, chunk)
});


