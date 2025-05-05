/// <reference path="jquery.d.ts" />
function func(){
 
  let el_h = $(window).height();
  let head_h =
    $("header").outerHeight(true) +
    $("footer").outerHeight(true) +
    $("h1").outerHeight(true);
  $(".sticky-under-top").css({ "max-height": el_h - head_h });
}
$(document).ready(function () {
  func()
  $(window).on("resize", function () {
    func()
  });
});
