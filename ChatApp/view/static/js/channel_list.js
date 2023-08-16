function myFunction() {
  const filter = document.getElementById('myInput').value.toUpperCase();
  const li = document.getElementsByTagName('li');
    
    for (i = 0; i < li.length; i++) {
      txtValue = li[i].textContent;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }
