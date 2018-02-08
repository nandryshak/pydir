function dropdown(element) {
  var target = document.getElementById(element.id.split('_')[1])
  if (element.checked) { target.style.display = "block"; }
  else { target.style.display = "none"; }
}
