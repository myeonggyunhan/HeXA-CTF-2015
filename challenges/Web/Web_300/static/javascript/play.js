/*
 * Chromeless player has no controls.
 */

// Update a particular HTML element with a new value
function updateHTML(elmId, value) {
  document.getElementById(elmId).innerHTML = value;
}

// This function is called when an error is thrown by the player
function onPlayerError(errorCode) {
  alert("An error occured of type:" + errorCode);
}

// This function is called when the player changes state
function onPlayerStateChange(newState) {
  updateHTML("playerState", newState);
}

// Display information about the current state of the player
function updatePlayerInfo() {
  // Also check that at least one function exists since when IE unloads the
  // page, it will destroy the SWF before clearing the interval.
  if(ytplayer && ytplayer.getDuration) {
    updateHTML("videoDuration", ytplayer.getDuration());
    updateHTML("videoCurrentTime", ytplayer.getCurrentTime());
    updateHTML("bytesTotal", ytplayer.getVideoBytesTotal());
    updateHTML("startBytes", ytplayer.getVideoStartBytes());
    updateHTML("bytesLoaded", ytplayer.getVideoBytesLoaded());
    updateHTML("volume", ytplayer.getVolume());
  }
}

// Allow the user to set the volume from 0-100
function setVideoVolume() {
  var volume = parseInt(document.getElementById("volumeSetting").value);
  jQuery.ajax({
        type:"POST",
        url:"/volume/",
        timeout:10000,
        data: 'volume='+document.getElementById("volumeSetting").value+''
      });
  if(isNaN(volume) || volume < 0 || volume > 100) {
    alert("Please enter a valid volume between 0 and 100.");
  }
  else if(ytplayer){
    ytplayer.setVolume(volume);
  }
}

function playVideo() {
  if (ytplayer) {
    ytplayer.playVideo();
  }
}

function pauseVideo() {
  if (ytplayer) {
    ytplayer.pauseVideo();
  }
}

function muteVideo() {
  if(ytplayer) {
    ytplayer.mute();
  }
}

function unMuteVideo() {
  if(ytplayer) {
    ytplayer.unMute();
  }
}


// This function is automatically called by the player once it loads
function onYouTubePlayerReady(playerId) {
  ytplayer = document.getElementById("ytPlayer");
  // This causes the updatePlayerInfo function to be called every 250ms to
  // get fresh data from the player
  setInterval(updatePlayerInfo, 250);
  updatePlayerInfo();
  ytplayer.addEventListener("onStateChange", "onPlayerStateChange");
  ytplayer.addEventListener("onError", "onPlayerError");
  //Load an initial video into the player
  ytplayer.cueVideoById(playerId);
}

// The "main method" of this sample. Called when someone clicks "Run".
function loadPlayer() {
  // Lets Flash from another domain call JavaScript
  var params = { allowScriptAccess: "always" };
  // The element id of the Flash embed
  var atts = { id: "ytPlayer" };
  // All of the magic handled by SWFObject (http://code.google.com/p/swfobject/)
  swfobject.embedSWF("http://www.youtube.com/apiplayer?" +
                     "&enablejsapi=1&playerapiid=ytplayer", 
                     "videoDiv", "0", "0", "8", null, null, params, atts);
}
function _run() {
  loadPlayer();
}
google.setOnLoadCallback(_run);





//Searching music list using Ajax

function findData(text){
  jQuery.ajax({
        type:"POST",
        url:"/music/",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        timeout:10000,
        data: 'name='+document.getElementById('musicName').value + '',
        success : function(data) {
              // TODO
              data_s = data.replace (/\\x/g, "\%");
              data_s = unescape(data_s);
              data = jQuery.parseJSON(data_s);

              //Remove list first
              function deleteResult() {
		$(".music_list").remove();
              }
		deleteResult();

              //print list
              function showResult(name, id, num){
                totalBox = document.createElement('div');
                $(totalBox).addClass("music_list")
                           .attr("id", "result"+num);

                nameBox = document.createElement('div');
                $(nameBox).addClass("musicNameBox");

                addBox = document.createElement('div'); 
                $(addBox).addClass("musicAddBox");
                
                musicText = document.createElement('p');
                $(musicText).addClass("musicName")
                            .text(decodeURIComponent(escape(name)))
                            .attr('href', "javascript:void(0);")
                            .click(function() {
                              onYouTubePlayerReady(id);
                              playVideo();
                            });
                
                musicAdd = document.createElement('a');
                $(musicAdd).addClass("musicAdd")
                           .text("추가")
                           .attr('href', "javascript:void(0);")
                           .click(function() {
                              musicAddList(name, id);
                            });

                $('#searchList').append(totalBox)
                $(totalBox).append(nameBox)
                $(nameBox).append(musicText);
                $(totalBox).append(addBox)
                $(addBox).append(musicAdd);
                
              }
              console.log(data.hasOwnProperty);
              var num=0;
              for (var i = Object.keys(data).length - 1; i >= 0; i--) {
                showResult(data[i].name, data[i].id, num);
                num++;
              };

        },
        complete : function(data) {
             // 통신이 실패했어도 완료가 되었을 때 이 함수를 타게 된다.
             // TODO

        },
        error : function(xhr, status, error, data) {
             alert("code:"+xhr.status + " " + error + " " + data);
        }
    });
}

function findData2(text){
  var xhr = new XMLHttpRequest();
  xhr.open('POST', './music/');
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  var data = '';
  data += 'name='+document.getElementById('musicName').value + '';
  xhr.send(data);
  xhr.onreadystatechange = alertContents;

  function alertContents() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var result = eval(xhr.responseText);
        alert(eval(result));
        //showResult(name, id);

        function showResult(name, id){
          object = document.getElementById("searchList");
          var totalBox = document.createElement('div');
          var nameBox = document.createElement('div');
          var delBox = document.createElement('div'); 
          var musicText = document.createElement('a');
          var musicDel = document.createElement('a');

          //var musicText = document.createTextNode(text);

          totalBox.setAttribute('class', 'music_list');
          nameBox.setAttribute('class', 'musicNameBox');
          delBox.setAttribute('class', 'musicAddBox');
          musicText.setAttribute('class', 'musicName');
          musicDel.setAttribute('class', 'musicAdd');
          musicText.setAttribute('href', 'javascript:void(0);');
          musicText.setAttribute('onclick', 'onYouTubePlayerReady('+id+');playVideo();');
          musicText.innerHTML = name;
          musicDel.innerHTML = "추가";

          object.appendChild(totalBox).appendChild(nameBox).appendChild(musicText);
          totalBox.appendChild(delBox).appendChild(musicDel)
        }
        //alert(xhr.responseText);
      } else {
        alert('There was a problem with the request.');
      }
    }
  }
}

function musicDelete (list_id) {
  alert('#'+list_id);
  $('#list_'+list_id).each(function() {
    $(this).remove();
  });
}

//Music Add
i=1;
function musicAddList(name,id){
  
  list_id = "list_"+i;
  totalBox = document.createElement('div');
  $(totalBox).addClass("music_list_save")
             .attr("id", list_id);
  

  nameBox = document.createElement('div');
  $(nameBox).addClass("musicNameBox");

  delBox = document.createElement('div'); 
  $(addBox).addClass("musicDelBox");
  
  musicText = document.createElement('p');
  $(musicText).addClass("musicName")
              .text(decodeURIComponent(escape(name)))
              .attr('href', "javascript:void(0);")
              .click(function() {
                onYouTubePlayerReady(id);
                playVideo();
              });
  
  musicDel = document.createElement('a');
  $(musicDel).addClass("musicDel")
             .text("삭제")
             .attr('href', "javascript:void(0);")
             .attr('id', i)
             .click(function() {
                musicDelete($(this).attr("id"));
              });
 
  //var musicText = document.createTextNode(text);  

  $('#playerList').append(totalBox);
  $(totalBox).append(nameBox);
  $(nameBox).append(musicText);
  $(totalBox).append(delBox);
  $(delBox).append(musicDel);
  i++;
}


