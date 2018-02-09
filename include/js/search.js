// Grab the JSON and store it locally.
var _Tree = JSON.parse(jsonText);

var searchTerm = getQueryVariable('query');


document.getElementById('file-list').innerHTML = '<tr class="listing-item"><td class=""></td><td>Searching...</td><td><small class="text-muted"></small></td><td><small class="file-size text-muted"></small></td></tr>';

if (searchTerm) {
  document.getElementById('search-box').setAttribute("value", searchTerm);

  // Initalize lunr with the fields it will be searching on. I've given title
  // a boost of 10 to indicate matches on this field are more important.
  var idx = lunr(function () {
    this.ref('index');
    this.field('name', { boost: 10 });

    for (var i = 0, emp; i < _Tree.length; i++) { // Add the data to lunr
      this.add({
        'index': i,
        'name': _Tree[i].name
      });
    }
  });

  displaySearchResults(idx.search(searchTerm + "~1"), _Tree);
}



function getQueryVariable(variable) { // To extract URL query information for search
  var query = window.location.search.substring(1);
  var vars = query.split('&');

  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split('=');

    if (pair[0] === variable) {
      return decodeURIComponent(pair[1].replace(/\+/g, '%20'));
    }
  }
}


function displaySearchResults(results, store) {
  var searchResults = document.getElementById('file-list');
  if (results.length) { // Are there any results?
    var appendString = '';

    for (var i = 0; i < results.length; i++) {  // Iterate over the results
      var item = store[results[i].ref];
      if(item) {
        appendString += '<tr class="listing-item" onclick="window.location.href=\'' + item.path + '\'">';
        appendString += '<td class=""></td>'
        appendString += '<td><a class="file-name" draggable="true" href="' + item.path + '">' + item.name + '<br> <small class="text-muted">' + item.path.trim('.') + '</small></a></td>'
        appendString += '<td><small class="text-muted">' + item.lastmodified + '</small></td>'
        appendString += '<td><small class="file-size text-muted">' + item.filesize + '</small></td></tr>'
      }
    }
    searchResults.innerHTML = appendString;

  } else {
    searchResults.innerHTML = '<tr class="listing-item"><td class=""></td><td>No Matches Found</td><td><small class="text-muted"></small></td><td><small class="file-size text-muted"></small></td></tr>';
  }
}

// Better Trim Methods

String.prototype.trimLeft = function(charlist) {
  if (charlist === undefined)
    charlist = "\s";

  return this.replace(new RegExp("^[" + charlist + "]+"), "");
};

String.prototype.trimRight = function(charlist) {
  if (charlist === undefined)
    charlist = "\s";

  return this.replace(new RegExp("[" + charlist + "]+$"), "");
};

String.prototype.trim = function(charlist) {
  return this.trimLeft(charlist).trimRight(charlist);
};
