$(document).ready(function(){
  $('.order-item').on('click', function(ev){
    let id = $(this).data('order-id')
   $.get(
    "/order/"+id,
    function(data){
      $('#order_modal .modal-body').html(data)
    }
   )
  })
})