import json
import traceback

def generate_almanac_from_json(in_filename, out_filename):

    generate_almanac(load_json_from_file(in_filename), out_filename)

def load_json_from_file(filename):

    with open(filename + ".json", "r", encoding="utf-8") as file:

        out = json.loads(file.read())

    return out

def generate_almanac(in_json, filename):

    with open(filename + ".html", "w", encoding="utf-8") as file:
        file.write('''
        
<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Roboto+Condensed&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=PT+Serif&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Nova+Script&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap" rel="stylesheet">
    <style>
        html,body{height:100%;font-size:16px;scroll-behavior:smooth;}
        body{
            background:#333;
            color:#eee;
            font-family:'PT Serif', serif;
            margin:0;
            text-align:justify;
            scrollbar-color:#999 #666;
            scrollbar-width:thin;
            overflow-x:hidden;
        }
        table{
            border:1px solid rgba(51,51,51,0.35);
            margin:0 auto;
            background-color:rgba(255,255,255,0.15);
        }
        a{text-decoration:none;color:#339}
        a:hover{text-decoration:underline;color:#66c}
        tbody tr:nth-child(even), th{background-color:rgba(255,255,255,0.65);}
        td,th{padding:4px;}
        *::-webkit-scrollbar {
            width:10px;
            height:10px;
        }
        *::-webkit-scrollbar-track {
            background:#666;
        }
        *::-webkit-scrollbar-thumb {
            background:#999;
        }
        h1, h2, h3, h4, h5, h6, h7 {
            margin:0.2rem 0 0.2rem 0;
            font-family: 'Nova Script', cursive;
            text-transform:uppercase;
        }
        h1, h2{font-size:2.4rem}
        h3, h4, h5, h6, h7 {font-size:1.2rem}
        hr{width:80%;border:1px solid}
        ol.nav {
            flex:0 0 124px;
            font-family:'Roboto Condensed',sans-serif;
            font-size:1rem;
            list-style:none;
            margin:0;
            padding:1vh 0 0 0;
            overflow-x:hidden;
            overflow-y:auto;
            position:fixed;
            height:100vh;
            z-index:1;
            background:#333;
        }
        ol.nav > li {
            padding-left: 0.2rem;
        }
        .nav a{
            text-align:center;
            vertical-align:bottom;
            text-decoration:none;
            color:#eee;
        }
        .nav a:hover{
            text-decoration:underline;
            box-shadow: 0 0 0.1em #333;
        }
        .almanac-row{
            max-width:924px;
            overflow-x: hidden;
            margin:auto;
        }
        .almanac-viewport {
            list-style:none;
            margin:0;
            padding:0;
            display: flex;
            align-items: stretch;
            justify-content: space-between;
            flex-flow: column nowrap;
            overflow-x:hidden;
            max-width:800px;
            margin-left:124px;
        }
        .page {
            list-style:none;
            flex: none;
            margin:0 0.6rem 0.6rem 0;
            position:relative;
        }
        .page img{
            max-width:90vw;
        }
        .page-contents{
            margin:auto;
            padding:4.8rem 3.7rem;
            display:flex;
            flex-flow: column nowrap;
            align-items: center;
            background-repeat: no-repeat;
            background-size: 19.2rem;
            background-position: top;
            background-position-y: 2.4rem;
            color:#333;
        }
        .spacer{height:11rem}
        #synopsis > .page-contents > p,
        #overview > .page-contents > p,
        #changelog > .page-contents > p {
            width:60%;
        }
        .donate {
            list-style:none;
            flex: none;
            position:relative;
            text-align:center
        }

        /*paper effect*/
        .page::before{
            content:"";
            position:absolute;
            left:0;
            top:0;
            right:0;
            bottom:0;
            box-shadow:0 0 4.5rem #966e49 inset;
            z-index:-1;
            background-color:#eadbca;
        }

        .generated-by{
        list-style:none;
        padding:0 0 1rem 0;
        text-align:center;
        font-size:0.8rem;
        flex:none;
        font-family:'Roboto Condensed',sans-serif;
        }
        .generated-by a{
            color:#ccf
        }
        .team{
            font-family: 'MedievalSharp', cursive;
            writing-mode:vertical-rl;
            text-orientation: upright;
            text-transform: uppercase;
            position: absolute;
            top: 4.8rem;
            left: 3.2rem;
            letter-spacing:-0.4rem;
            width:unset;
            font-size:1.8rem;
            margin:0;
        }
        p{
            margin-top:0.4rem;
            margin-bottom:0.4rem;
        }
        .inline-logo{
            float:left;
            margin:-0.4rem 0.4rem 0 -3.2rem;
            width:6.4rem;
        }
        #synopsis > .page-contents{
            font-family: 'MedievalSharp', cursive;
            color:#933;
        }
        .ability{
            width:60%;
            font-family:'Roboto Condensed',sans-serif;
            text-align:center;
        }
        .flavor{
            width:60%;
            font-style:italic;
            color:#704c29;
            text-align:center;
            font-size:0.8rem;
        }
        .overview, .example, .how-to-run, .attribution {
            width:80%;
        }
        .tip > p {
            width:80%;
            color:#933;
            padding:20px;
            background:rgba(255, 255, 255, 0.35);
            border:4px solid #933;
            margin-left:auto;
            margin-right:auto;
        }

        /* big letter */
        #synopsis > .page-contents > p:nth-child(1)::first-letter {
            font-size:2rem;
        }
        .overview > p:nth-child(1)::first-letter {
            font-family: 'MedievalSharp', cursive;
            font-size: 5rem;
            float:left;
            line-height:0.7;
            margin: 0 0.3rem 0 -0.4rem;
        }
        .overview > p:nth-child(1) {
            min-height: 3.5rem;
        }

        /* bullets */
        .overview > p + p {
            position:relative;
            margin-left:1.3rem;
        }
        .overview > p + p::before {
            content:'â€¢';
            font-size:1.4rem;
            position:absolute;
            line-height:0.9;
            top:0;
            left:-1.4rem;
        }
        .page::before{background-image:url('/img/paper.png');}

        .townsfolk h1,
        .townsfolk h2,
        .townsfolk h3,
        .townsfolk h4,
        .townsfolk h5,
        .townsfolk h6,
        .townsfolk .ability,
        .townsfolk .team,
        .townsfolk .overview > p:nth-child(1)::first-letter,
        .townsfolk .overview > p + p::before {
            color:#003fb2;
        }
        .townsfolk hr {
            border-color:#003fb2;
        }
        .nav > li.townsfolk {
            background: #1f65ff55;
        }

        .outsider h1,
        .outsider h2,
        .outsider h3,
        .outsider h4,
        .outsider h5,
        .outsider h6,
        .outsider .ability,
        .outsider .team,
        .outsider .overview > p:nth-child(1)::first-letter,
        .outsider .overview > p + p::before {
            color:#006893;
        }
        .outsider hr {
            border-color:#006893;
        }
        .nav > li.outsider {
            background: #46d5ff55;
        }

        .minion h1,
        .minion h2,
        .minion h3,
        .minion h4,
        .minion h5,
        .minion h6,
        .minion .ability,
        .minion .team,
        .minion .overview > p:nth-child(1)::first-letter,
        .minion .overview > p + p::before {
            color:#9f0000;
        }
        .minion hr {
            border-color:#9f0000;
        }
        .nav > li.minion {
            background: #ff690055;
        }

        .demon h1,
        .demon h2,
        .demon h3,
        .demon h4,
        .demon h5,
        .demon h6,
        .demon .ability,
        .demon .team,
        .demon .overview > p:nth-child(1)::first-letter,
        .demon .overview > p + p::before {
            color:#940000;
        }
        .demon hr {
            border-color:#940000;
        }
        .nav > li.demon {
            background: #ce010055;
        }

        .traveler h1,
        .traveler h2,
        .traveler h3,
        .traveler h4,
        .traveler h5,
        .traveler h6,
        .traveler .ability,
        .traveler .team,
        .traveler .overview > p:nth-child(1)::first-letter,
        .traveler .overview > p + p::before {
            color:#553412;
        }
        .traveler hr {
            border-color:#553412;
        }
        .nav > li.traveler {
            background: linear-gradient(90deg, #1f65ff55 49%,#ce010055 51%);
        }

        .fabled h1,
        .fabled h2,
        .fabled h3,
        .fabled h4,
        .fabled h5,
        .fabled h6,
        .fabled .ability,
        .fabled .team,
        .fabled .overview > p:nth-child(1)::first-letter,
        .fabled .overview > p + p::before {
            color:#553412;
        }
        .fabled hr {
            border-color:#553412;
        }

        .jinxes h1,
        .jinxes h2,
        .jinxes h3,
        .jinxes h4,
        .jinxes h5,
        .jinxes h6,
        .jinxes .ability,
        .jinxes .team,
        .jinxes .overview > p:nth-child(1)::first-letter,
        .jinxes .overview > p + p::before {
            color:#333;
        }
        .jinxes hr {
            border-color:#333;
        }

        .nav > li.fabled {
            background: #ffe91f55;
        }

        .characterImage {
            max-width:22rem;
            height:22rem;
            margin-top: -2rem;
            margin-bottom: -6.5rem;
        }
        .nightOrder {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap:5rem;
            margin:1rem;
        }
        .nightOrderList {
            display: grid;
            grid-template-columns: auto 1fr;
            gap:6px;
            align-items: center;
        }
        .nightOrderListName {
            font-size:1.2rem;
        }
        .nightOrderListIcon {
            max-width: 60px;
            height: 60px;
            margin-bottom: -20px;
        }
        .firstNightColumn {
            align-self: start;
        }
        .otherNightsColumn {
            /*transform:rotate(180deg);*/
            align-self: end;
        }


        @media only screen and (max-width:799px){
            .page-contents{
                padding:8vw;
                background-position-y:1vw;
                background-size:48vw;
            }
            .spacer{
                height:26vw;
            }
            html{font-size:16px;}
            .flavor p{font-size:0.875rem;}

            /* big letter and bullets*/
            .overview > p:nth-child(1)::first-letter {font-size: 4rem;}

            h1, h2{font-size:2.25rem}
            h3, h4, h5, h6, h7 {font-size:1.125rem}
            .team{
                font-size:1.25rem;
                letter-spacing:-0.25rem;
                left:8vw;
                top:8vw;
            }
        }
        @media only screen and (max-width:650px){
            .page {
                margin-right:0;
            }
            .page-contents{
                background-size:57vw;
            }
            .spacer{
                height:31vw;
            }
            ol.nav {
                overflow-x: auto;
                overflow-y: hidden;
                width:100%;
                display:flex;
                height:unset;
                padding: 0.25rem 0;
            }
            .nav li{
                flex:1 0 auto;
                margin:0 5px;
            }
            .almanac-viewport{
                margin-left:0px;
                margin-top:45px;
            }
            #synopsis > .page-contents > p,
            #overview > .page-contents > p,
            #changelog > .page-contents > p {width:100%}
            .team{
                font-size:3vw;
                letter-spacing:0;
                top:10vw;
            }
            .ability, .flavor, .overview, .example, .how-to-run, .attribution{
                width:80vw;
            }
            .tip > p{width:75vw;}
            .inline-logo{margin-left:0}
            .nightOrder {gap:1rem;}
        }
        @media only screen and (max-width:450px){
            h1, h2{font-size:8vw}
            h3, h4, h5, h6, h7 {font-size:4vw}
            .nightOrderListIcon{
                height: 6vw;
                margin-bottom: -2vw;
                margin-right: -1vw;
            }
        }
        @media only screen and (max-width:400px){
            h1, h2{font-size:32px}
            h3, h4, h5, h6, h7 {font-size:16px}
            .nightOrderListIcon{
                height: 24px;
                margin-bottom: -8px;
                margin-right: 0;
            }
            .nightOrder{display:block}
            .nightOrderList{margin-bottom:1rem}
        }

        .center{
            margin: auto;
            text-align: center;
        }
    </style>\n''')    
        file.write(f"<title>{in_json[0]['name']}</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("<div class=\"almanac-row\">\n")
        file.write("<ol class=\"nav\">\n")

        for character in in_json[1:]:
            if type(character) != str:
                file.write(f"<li class=\"{character['team']}\"><a href=\"#{character['id']}\">{character['name']}</a></li>\n")
        file.write("<a href=\"#nightOrder\">Night Order</a></li>\n")
        file.write("</ol>\n")
        file.write("<ol class=\"almanac-viewport\">\n")

        for character in in_json[1:]:

            if type(character) != str:
            
                file.write(f"<li class=\"page\" id=\"{character['id']}\">\n")
                file.write(f"<div class=\"page-contents {character['team']}\">\n")

                if character.get('image') is not None:

                    if type(character['image']) == str:

                        file.write(f"<img src=\"{character['image']}\" class=\"characterImage\" alt=\"\"/>")
                    
                    else:

                        file.write(f"<img src=\"{character['image'][0]}\" class=\"characterImage\" alt=\"\"/>")

                file.write(f"<h2>{character['name']}</h2>\n")
                file.write(f"<p class=\"ability\">{character['ability']}</p>\n")
                file.write("<hr>\n")
                
                if character.get('flavor') is not None:

                    file.write(f"<div class=\"flavor\">{character['flavor']}</div>\n")
                
                if character.get('hook') is not None or character.get('summary') is not None:

                    overview_string = f"<div class=\"overview\">"
                    
                    if character.get('hook') is not None:
                        overview_string += f"<p>{character['hook']}</p>\n"
                    
                    if character.get('summary') is not None:
                        overview_string += "<ul>\n"
                        for line in character['summary']:
                            overview_string += f"<li>{line}</li>\n"
                        overview_string += "</ul>\n"
                    overview_string += "</div>\n"

                    file.write(overview_string)
                    
                
                if character.get('examples') is not None:

                    file.write("<h3>Examples</h3>\n")
                    file.write("<div class=\"example\">\n")

                    for example in character['examples']:

                        file.write(f"<p>{example}</p>\n")
                    
                    file.write("</div>\n")
                
                if character.get('howtorun') is not None:

                    file.write("<h3>How to Run</h3>\n")
                    file.write("<div class=\"how-to-run\">\n")
                    file.write(f"<p>{character['howtorun']}</p>\n")
                    file.write("</div>\n")
            
                if character.get('tip') is not None:

                    file.write("<div class=\"tip\">\n")
                    file.write(f"<p>{character['tip']}</p>\n")
                    file.write("</div>\n")
                
                file.write(f"<p class=\"team\">{character['team'][0].upper() + character['team'][1:]}</p>")
                file.write("</div>\n")
                file.write("</li>\n")
        
        file.write("<li class=\"page\" id=\"nightOrder\">\n")
        file.write("<div class=\"page-contents\">\n")
        file.write("<h2>Night Order</h2>\n")

        file.write("<div class=\"nightOrder\">\n")
        file.write("<div class=\"firstNightColumn\">\n")
        file.write("<h3>First Night</h3>\n")
        file.write("<div class=\"nightOrderList\">")

        first_night_orders = [in_json[x] for x in range(len(in_json[1:])) if in_json[x].get("firstNight", None) is not None]
        first_night_orders.sort(key = lambda x: x["firstNight"])

        for character in first_night_orders:

            if character.get('image') is not None:
                file.write(f"<img class=\"nightOrderListIcon\" src=\"{character['image']}\" alt=\"\"/>")
            else:
                file.write("<div></div>")
            file.write(f"<div class=\"nightOrderListName\">\n{character['name']}</div>\n")
        
        file.write("</div></div>\n")
        file.write("<div class=\"otherNightsColumn\">\n")
        file.write("<h3>Other Nights</h3>\n")
        file.write("<div class=\"nightOrderList\">")

        other_night_orders = [in_json[x] for x in range(len(in_json[1:])) if in_json[x].get("otherNight", None) is not None]
        other_night_orders.sort(key = lambda x: x["otherNight"])

        for character in other_night_orders:

            if character.get('image') is not None:
                file.write(f"<img class=\"nightOrderListIcon\" src=\"{character['image']}\" alt=\"\"/>")
            else:
                file.write("<div></div>")
            file.write(f"<div class=\"nightOrderListName\">\n{character['name']}</div>\n")
        
        file.write("</div></div></div></div></li></ol></div></body></html>")

def main(in_name = "", out_name = ""):
    
    if (in_name == ""):
        in_name = input("Enter Source Filename (without .json): ")
    if (out_name == ""):
        out_name = input("Enter Outputted Filename (without .html): ")
    try:
        generate_almanac_from_json(in_name, out_name)
    except Exception as e:
        print(traceback.format_exc())
        print("Something went wrong. Check the json file exists and is formatted correctly. Alternatively, forward this to Fragments/Quorg (they'll need the JSON). Alternatively alternatively, cry.")

if __name__ == "__main__":
    main("collection", "index")
    # If anyone else is using this god-awful code (why), change the above to the right file :)