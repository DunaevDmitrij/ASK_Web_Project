$(function(){
  // Vote maker
  $('.voter').click(function(){
    var $voter = $(this)
    var $rater = $("#rating")
    if ($voter.attr('id')=="js-rateUp"){
      var votePoint = 1;
      var rateData = true;
    }
    else{
      var votePoint = -1;
      var rateData = false;
    }
    dataToSend = {userID:parseInt($("#authorID").val()),
                  questionID:parseInt($("#questionID").val()),
                  rate:rateData};
    $.post("/ajax/rate",$.toJSON(dataToSend),function(status){
      if (status == "success"){
        var num = parseInt($rater.text())
        $rater.text(num+votePoint);
        $(".voter").hide();
      }
    });
    return false;
  });
  // Comments
  $('.comment').submit(function(){
    var $form = $(this);
    dataToSend = {text:$form.children("textarea").val(),
                  author:parseInt($("#authorID").val()),
                  type:parseInt($form.children("input[name=typeID]").val()),
                  id:parseInt($form.children("input[name=elemID]").val())};
    if (dataToSend["text"] !== "") {
      $.post("/ajax/comment",$.toJSON(dataToSend),function(answer){
        $form.children("textarea").val("");
        $form.parent().append("       <p>"+dataToSend["text"]+"</p><hr>");
        $("#dataInOverlay").text("Your comment added");
        $("#overlay").show();
      });
    }
    else {
      $("#dataInOverlay").text("Please, enter data in textarea before sending data");
      $("#overlay").show();
    }
    return false;
  });
  // Closing comments block
  $(".comms").click(function(){
    $("#"+$(this).attr("id")+"Comments").toggle();
  });
  // Answer
  $('#answerForm').submit(function(){
    var $form = $(this);
    dataToSend = {text:$form.children("textarea").val(),
                  author:parseInt($('#authorID').val()),
                  question:parseInt($('#questionID').val())};
    if (dataToSend["text"] !== "") {
      $.post("/ajax/answer",$.toJSON(dataToSend),function(answer){
        $form.children("textarea").val("");
        $form.parent().append('    <div>'+dataToSend["text"]+'<div><hr>');
        $("#dataInOverlay").text("Your answer added");
        $("#overlay").show();
      });
    }
    else {
      $("#dataInOverlay").text("Please, enter data in textarea before sending data");
      $("#overlay").show();
    }
    return false;
  });
  // Answer righter
  $(".righter").click(function(){
    $btn = $(this);
    dataToSend = {aID:parseInt($btn.attr("id"))}
    $.post("/ajax/solver",$.toJSON(dataToSend),function(answer){
      $("#dataInOverlay").val("You've chosen right answer");
      $("#overlay").show();
      $(".righter").hide();
    });
    return false;
  });
});
