// Variable Declarations with default values.
var _Tree;
var _lunrIndex;

function init() {
  // Grab the JSON and store it locally.
  loadJSON(function(response) { console.log(response); this._Tree = JSON.parse(response);});
}
