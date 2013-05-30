$(function(){
  $("#js-TEST").click(function(){
    $.get("/ajax/indexAnswer",function(data) {
      json=$.parseJSON(data);
      alert(json["bool"])
    });
  });
  $("#ajax").submit(function(){
    dataToSend = {sendData:$("#js-text").val()};
    $.post("/ajax/indexSend",$.toJSON(dataToSend),function(answer) {
      alert(answer+"\n"+typeof(answer));
    });
    return false;
  });
});
