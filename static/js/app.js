// new DataTable('#example');
// let table = new DataTable('#example');




// var carouselWidth = $(".carousel-inner")[0].scrollWidth;
// var cardWidth = $(".carousel-item").width();
// var scrollPosition = 0;

// $(".carousel-control-next").on("click", function () {
//     if (scrollPosition < (carouselWidth - cardWidth * 4)) { //check if you can go any further
//       scrollPosition += cardWidth;  //update scroll position
//       $(".carousel-inner").animate({ scrollLeft: scrollPosition },600); //scroll left
//     }
// });

// $(".carousel-control-prev").on("click", function () {
//     if (scrollPosition > 0) {
//       scrollPosition -= cardWidth;
//       $(".carousel-inner").animate(
//         { scrollLeft: scrollPosition },
//         600
//       );
//     }
// });

// var multipleCardCarousel = document.querySelector(
//     "#carouselExampleControls"
// );
// if (window.matchMedia("(min-width: 768px)").matches) {
//     //rest of the code
//     var carousel = new bootstrap.Carousel(multipleCardCarousel, {
//       interval: false
//     });
// } else {
//     $(multipleCardCarousel).addClass("slide");
// }

// var carousel = new bootstrap.Carousel(multipleCardCarousel, {
//     interval: false,
//     wrap: false,
// });

// above code is for carousel

// Some code for getting the right subcategory upon choosing a main category

function myFunction() {
  let box_value = document.getElementById("category").value;
  if (box_value === "Tub") {
    document.getElementById("uniquergrptub").style.display  = "initial";
    document.getElementById("uniquergrpsanum").style.display  = "none";
  } else {
    document.getElementById("uniquergrptub").style.display  = "none";
    document.getElementById("uniquergrpsanum").style.display  = "initial";
  }
}

function myFunction2() {
  let box_value2 = document.getElementById("subcategory_sanum").value;
  if (box_value2 === "Petit") {
    document.getElementById("uniquergrpcategory").style.display  = "none";
    document.getElementById("uniquergrpsanum").style.display  = "none";
    document.getElementById("uniquergrptub").style.display  = "none";
    document.getElementById("uniquergrpfruit1").style.display  = "initial";
    document.getElementById("uniquergrpfruit2").style.display  = "initial";
    document.getElementById("uniquergrpcrunch1").style.display  = "initial";
    document.getElementById("uniquergrpsauce1").style.display  = "initial";
    document.getElementById("uniquergrpprompt").style.display  = "initial";
  } else if (box_value2 === "Regular"){
    document.getElementById("uniquergrpcategory").style.display  = "none";
    document.getElementById("uniquergrpsanum").style.display  = "none";
    document.getElementById("uniquergrptub").style.display  = "none";
    document.getElementById("uniquergrpfruit1").style.display  = "initial";
    document.getElementById("uniquergrpfruit2").style.display  = "initial";
    document.getElementById("uniquergrpfruit3").style.display  = "initial";
    document.getElementById("uniquergrpcrunch1").style.display  = "initial";
    document.getElementById("uniquergrpcrunch2").style.display  = "initial";
    document.getElementById("uniquergrpsauce1").style.display  = "initial";
    document.getElementById("uniquergrpprompt").style.display  = "initial";
  }
}

function myFunction3() {
  let box_value3 = document.getElementById("subcategory_tub").value;
  if (box_value3 === "Small") {
    document.getElementById("uniquergrpcategory").style.display  = "none";
    document.getElementById("uniquergrpsanum").style.display  = "none";
    document.getElementById("uniquergrptub").style.display  = "none";
    document.getElementById("uniquergrptopping1").style.display  = "initial";
    document.getElementById("uniquergrpprompt").style.display  = "initial";
  } else {
    document.getElementById("uniquergrpcategory").style.display  = "none";
    document.getElementById("uniquergrpsanum").style.display  = "none";
    document.getElementById("uniquergrptub").style.display  = "none";
    document.getElementById("uniquergrptopping1").style.display  = "initial";
    document.getElementById("uniquergrptopping2").style.display  = "initial";
    document.getElementById("uniquergrptopping3").style.display  = "initial";
    document.getElementById("uniquergrpprompt").style.display  = "initial";
  }
}

function myFunction4() {
  let box_value4 = document.getElementById("ask_user").value;
  if (box_value4) {
    document.getElementById("uniquergrpprompt").style.display  = "none";
    document.getElementById("uniquergrpcomboname").style.display  = "initial";
    document.getElementById("uniquergrpsubmit").style.display  = "initial";
  }
}



// function myFunction5() {
//   let box_value5 = document.getElementById("rating_here").value;
//   if (box_value5) {
//     console.log('Hello, this is pressed.')
//     document.getElementById("uniquergrpratinginitbutton").style.display  = "none";
//     document.getElementById("uniquergrpratingbyuser").style.display  = "initial";
//     document.getElementById("uniquergrpcommentbyuser").style.display  = "initial";
//     document.getElementById("uniquergrpsubmitrating").style.display  = "initial";
//   }

// }

// function myFunction6() {
//   let box_value6 = document.getElementById("submit").value;
//   if (box_value6) {
//     document.getElementById("uniquergrpratingbyuser").style.display  = "none";
//     document.getElementById("uniquergrpcommentbyuser").style.display  = "none";
//     document.getElementById("uniquergrpsubmitrating").style.display  = "none";
//   }
// }
