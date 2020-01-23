// formvalidation
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
// endofformvalidation

// categorydrpdown
$(document).ready(function(){
  $('.dropdown-submenu a.test').on("click", function(e){
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
  });
});



// accordion
$(document).ready(function(){
    // Add minus icon for collapse element which is open by default
    $(".collapse.show").each(function(){
        $(this).prev(".card-header").find(".fa").addClass("fa-minus").removeClass("fa-plus");
    });
    // Toggle plus minus icon on show hide of collapse element
    $(".collapse").on('show.bs.collapse', function(){
        $(this).prev(".card-header").find(".fa").removeClass("fa-plus").addClass("fa-minus");
    }).on('hide.bs.collapse', function(){
        $(this).prev(".card-header").find(".fa").removeClass("fa-minus").addClass("fa-plus");
    });
});


// snackbar
function snackBar() {
  // Get the snackbar DIV
  var x = document.getElementById("snackbar");

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}

function snackBarA() {
  // Get the snackbar DIV
  var xA = document.getElementById("snackbarA");

  // Add the "show" class to DIV
  xA.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ xA.className = xA.className.replace("show", ""); }, 5000);
}



// When the user scrolls the page, execute myFunction
window.onscroll = function() {scrollA()};

function scrollA() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("myBar").style.width = scrolled + "%";
}



// editabletable
const $tableID = $('#table');
  const $BTN = $('#export-btn');
  const $EXPORT = $('#export');

  const newTr = `
 <tr>
  <td class="pt-3-half d-flex align-items-center " contenteditable="true">
      <div class="imagescrollimg m-0">
          <img src="../img/productimages/product1.jpg" alt="cartproduct">
      </div>
      <div class="cart-prod-name-wrapper pl-4">
          <p class="cart-prod-name-text">Infinix Hot S4, 6.2", 32GB + 3GB(Dual SIM), Blue</p>
      </div>

  </td>
  <td class="pt-3-half  " contenteditable="true">30</td>
  <td class="pt-3-half d-flex justify-content-center" contenteditable="true">
      <div class="slider-container">
          <button onclick="subtract()" class="slider-contents slider-contents-control border-right"><i class="fas fa-minus"></i></button>
          <span class="slider-contents slider-contents-center d-flex justify-content-center align-items-center" id="slider_count">0</span>
          <button onclick="add()" class="slider-contents slider-contents-control border-left"><i class="fas fa-plus"></i></button>
      </div>
  </td>
  <td class="pt-3-half" contenteditable="true">
      <div>
          <span class="">
              <button type="button" class="delete-button"><i class="far fa-heart"></i></button>
           </span>
           <span class="table-remove">
              <button type="button" class="delete-button"><i class="fas fa-trash"></i></button>
           </span>
      </div>
  </td>
  <td class="pt-3-half" contenteditable="true">Ksh 12,000</td>
  <td class="pt-3-half" contenteditable="true">Ksh 19,000</td>
</tr>`;

  $('.table-add').on('click', 'i', () => {

    const $clone = $tableID.find('tbody tr').last().clone(true).removeClass('hide table-line');

    if ($tableID.find('tbody tr').length === 0) {

      $('tbody').append(newTr);
    }

    $tableID.find('table').append($clone);
  });

  $tableID.on('click', '.table-remove', function () {

    $(this).parents('tr').detach();
  });

  $tableID.on('click', '.table-up', function () {

    const $row = $(this).parents('tr');

    if ($row.index() === 1) {
      return;
    }

    $row.prev().before($row.get(0));
  });

  $tableID.on('click', '.table-down', function () {

    const $row = $(this).parents('tr');
    $row.next().after($row.get(0));
  });

  // A few jQuery helpers for exporting only
  jQuery.fn.pop = [].pop;
  jQuery.fn.shift = [].shift;

  $BTN.on('click', () => {

    const $rows = $tableID.find('tr:not(:hidden)');
    const headers = [];
    const data = [];

    // Get the headers (add special header logic here)
    $($rows.shift()).find('th:not(:empty)').each(function () {

      headers.push($(this).text().toLowerCase());
    });

    // Turn all existing rows into a loopable array
    $rows.each(function () {
      const $td = $(this).find('td');
      const h = {};

      // Use the headers from earlier to name our hash keys
      headers.forEach((header, i) => {

        h[header] = $td.eq(i).text();
      });

      data.push(h);
    });

    // Output the result
    $EXPORT.text(JSON.stringify(data));
  });





  function add(){
    var sliderCount=document.getElementsByClassName('slider_count');
    var count = sliderCount.innerText;
    if((count)>10){

    }else{
     count ++;
     sliderCount.innerText =count;
    }

 }
 function subtract(){
    var sliderCount=document.getElementsByClassName('slider_count');
    var count = sliderCount.innerText
    if (count != '0') {
        count --;
        sliderCount.innerText =count;
    }

 }



