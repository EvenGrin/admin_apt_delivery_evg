/// <reference path="jquery.d.ts" />
$(document).ready(function () {
  let el_h = $(window).height();
  let head_h = $("header").outerHeight(true) + $("footer").outerHeight(true)+$("h1").outerHeight(true);
  $(".sticky-under-top").css({"max-height": el_h - head_h})
  $(window).on("resize", function () {
    let el_h = $(window).height();
    let head_h = $("header").outerHeight(true);
    $(".sticky-under-top").css({"max-height": el_h - head_h})
    // console.log(head_h)
  });
});
