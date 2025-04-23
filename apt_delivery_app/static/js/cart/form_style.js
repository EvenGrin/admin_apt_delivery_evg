// /// <reference path="jquery.d.ts" />
// window.stylizeForm = function () {
//   const form_ = $("form");
//   if (form_) {
//     form_.find("p").wrap("<div class='row w-100 is-invalid'></div>");

//     form_
//       .find("input")
//       .not("[type='checkbox'], [type='radio'], [type='submit'], [type='button'], [type='range'] ")
//       .addClass("form-control")
//       .wrap("<div></div>");

//     form_.find("select").addClass("form-select");
//     form_
//       .find("input[type=checkbox]")
//       .wrap("<div class='col-6 d-flex align-items-center'></div>");

//     form_.find("label").addClass("col-form-label");

//     form_.find("br").remove();

//     form_.find("span").addClass("my-3");

//     form_.find(".errorlist").addClass("text-danger m-0 mt-3 invalid-feedback");

//     form_.find(".helptext").addClass("small");
//   }
// };
// stylizeForm();
