document.addEventListener('DOMContentLoaded', 
function displayTime() {
    // define the variable for the date and time and function
    const now = new Date();
    // console.log(now)
    const time = showHours(now.getHours()) + addZero(now.getMinutes()) + addZero(now.getSeconds()) + addamPm(now.getHours());
   
    document.querySelector('#time').innerHTML = time;
    // let function run every second
    setInterval(displayTime, 1000);

    // define function for 12 hours
    function showHours (hours) {
        if (hours < 12 || hours == 12){
            return hours;
        }
        if (hours > 12) {
            return hours - 12;
        }
    }
    // Add a zero to the single digit
    function addZero(val) {
        if (val > 9) {
            return ':' + val;
        }
        return ':0' + val;
    }

    // Add am or pm
    function addamPm (period) {
        if (period < 12) {
            return ' AM';
        }
        return ' PM';
    }
});


document.addEventListener('DOMContentLoaded', function showDate() {
    const now = new Date();
    // Display Date
    const day = now.getDate();
    // console.log(day)
    const month = now.getMonth() + 1;
    // console.log(month)
    const year = now.getFullYear();
    // console.log(year)

    document.querySelector('#date').innerHTML = ` ${day} / ${month} / ${year}`
 
});

// script to toggle to dark mode
function dark_mode() {
   // change the body to dark mode
   var element = document.body;
   element.classList.toggle("dark-mode");
   
   // get the ppty of the checkbox
   var btn = document.querySelector('#dark_mode')
   
   // set the state of the check box to local storage
   localStorage.setItem('checked_status', btn.checked)
}

// checkbox reload
function chk_box_reload(){
   var element = document.body;

   // get the ppty of the checkbox
   var btn = document.querySelector('#dark_mode')

   // var element = document.body;
   if (localStorage.getItem('checked_status') == 'true') {
      // make the checkbox checkd
      btn.checked = true;
      element.classList.toggle("dark-mode");
   } else {
      // uncheck the checkbox
      btn.checked = false;
   }
  
}


// js for leave application page
function leave() {
   
   x = document.querySelector('#leave_app')
   document.querySelector('#leave_app').style.display = 'block';
   document.querySelector('#leave_form').style.display = 'none';
}

// js for leave application page
function load_form() {
   document.querySelector('#leave_app').style.display = 'none';
   document.querySelector('#leave_form').style.display = 'block';
}


// function to download files
function download() {
   fetch('/download')
   .then(response => response.json())
   .then(product => {
      // Print emails
      console.log(product);
      console.log('Clicked')

      // ... do something else with emails ...
   });
   
}

// hide employee list on load
function show_emp_list() {
   
   // x = document.querySelector('#leave_app')
   document.querySelector('#show_emp_list').style.display = 'block';
   document.querySelector('#hide_emp_list').style.display = 'none';
 
}

// Show emp_list
function hide_emp_list() {
   document.querySelector('#show_emp_list').style.display = 'none';
   document.querySelector('#hide_emp_list').style.display = 'block';
}


// function to confirm delete of product from sales db
function confirm_delete(product) {
   var dels = confirm('Are you sure you want to delete this?');
   if (dels) {
      fetch(`delete_product/${product}`, {
         method: 'GET',
         // body: product
       })
      location.reload();
   } 
}




// billing page simple applivation
// function hide_invoice() {
//    document.querySelector('#billing_form').style.display = 'block';
//    document.querySelector('#billing_invoice').style.display = 'none';
// }

// // show billing invoice
// function show_invoice() {
//    document.querySelector('#billing_form').style.display = 'none';
//    document.querySelector('#billing_invoice').style.display = 'block';
//    return false;
// }



// // single page application
// document.addEventListener('DOMContentLoaded', () => {
//    // hr page
//    document.querySelector('#hr_main').style.display = 'block';
//    document.querySelector('#hr_emp').style.display = 'none';
//    document.querySelector('#emp_info').style.display = 'none';
// })

// // hide and display page as appropriate in hr page
// function emp_list() {
//    document.querySelector('#hr_main').style.display = 'none';
//    document.querySelector('#hr_emp').style.display = 'block';
//    document.querySelector('#emp_info').style.display = 'none';
// }


// // hide and display page as appropriate in hr page
// function update_emp() {
//    document.querySelector('#hr_main').style.display = 'none';
//    document.querySelector('#hr_emp').style.display = 'none';
//    document.querySelector('#emp_info').style.display = 'block';
// }
 
 