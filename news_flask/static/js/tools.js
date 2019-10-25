String.prototype.format = function () {
    var values = arguments;
    return this.replace(/\{(\d+)\}/g, function (match, index) {
        if (values.length > index) {
            return values[index];
        } else {
            return "";
            }
        });
    };

    function HTML (link,title,source,time,comments,category,img=null){
        var type;
        switch(category){
            case "politics":
                type = "国内";
                break;
            case "foreign":
                type = "国际";
                break;
            case "finance":
                type = "财经";
                break;
            case "tec":
                type = "科技";
                break;
            case "sport":
                type = "体育";
                break;
            case "ent":
                type = "娱乐";
        }
//        console.log(type)
        if (img==null){
        html = '<div class="blogs" data-scroll-reveal="enter bottom over 1s">';
               html += '<h3 class="blogtitle"><a href="/{0}" target="_blank">{1}</a></h3>'
               html += ' <div class="bloginfo">'
               html += '     <ul>'
               html += '         <li class="category"><a href="/{2}">{3}</a></li>'
               html += '         <li class="author">{4}</li>'
               html += '         <li class="timer">{5}</li>'
               html += '         <li class="view"><span>{6}</span>评论</li>'
               html += '     </ul>'
               html += ' </div>'
               html += '</div>'
               result = html.format(link,title,category,type,source,time,comments)
        }else{
               html = '<div class="blogs" data-scroll-reveal="enter bottom over 1s">';
               html += '<h3 class="blogtitle"><a href="/{0}" target="_blank">{1}</a></h3>';
               html += '<span class="bplist"><a href="info.html" title="">';
               html += '<li style="float: left;"><img src="{2}" alt=""></li>';
               html += '</a></span>';
               html += '<div class="bloginfo">';
               html += '    <ul>';
               html += '      <li class="category"><a href="/{3}">{4}</a></li>';
               html += '       <li class="author">{5}</li>';
               html += '       <li class="timer">{6}</li>';
               html += '       <li class="view"><span>{7}</span>评论</li>';
               html += '    </ul>';
               html += '</div>';
               html += '</div>';
               html += '</div>';
               result = html.format(link,title,img,category,type,source,time,comments)
        }
        return result
    };