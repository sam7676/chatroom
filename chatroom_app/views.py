from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
import datetime
import json

from chatroom_app.models import *

# Dictionary containing all colours listed on Wikipedia along with the corresponding
# colour code
color_dict = {"absolutezero":"#0048BA",
              "acidgreen":"#B0BF1A","aero":"#7CB9E8","africanviolet":"#B284BE","airsuperiorityblue":"#72A0C1","aliceblue":"#F0F8FF","alizarin":"#DB2D43","alloyorange":"#C46210","almond":"#EFDECD","amaranthdeeppurple":"#9F2B68","amaranthpink":"#F19CBB","amaranthpurple":"#AB274F","amazon":"#3B7A57","amber":"#FFBF00","amethyst":"#9966CC","androidgreen":"#3DDC84","antiquebrass":"#CD9575","antiquebronze":"#665D1E","antiquefuchsia":"#915C83","antiqueruby":"#841B2D","antiquewhite":"#FAEBD7","apricot":"#FBCEB1","aqua":"#00FFFF","aquamarine":"#7FFFD4","arcticlime":"#D0FF14","artichokegreen":"#4B6F44","arylideyellow":"#E9D66B","ashgray":"#B2BEB5","atomictangerine":"#FF9966","aureolin":"#FDEE00","azure":"#007FFF","azure(x11/webcolor)":"#F0FFFF","babyblue":"#89CFF0","babyblueeyes":"#A1CAF1","babypink":"#F4C2C2","babypowder":"#FEFEFA","baker-millerpink":"#FF91AF","bananamania":"#FAE7B5","barbiepink":"#DA1884","barnred":"#7C0A02","battleshipgrey":"#848482","beaublue":"#BCD4E6","beaver":"#9F8170","beige":"#F5F5DC","b'dazzledblue":"#2E5894","bigdiporuby":"#9C2542","bisque":"#FFE4C4","bistre":"#3D2B1F","bistrebrown":"#967117","bitterlemon":"#CAE00D","black":"#000000","blackbean":"#3D0C02","blackcoral":"#54626F","blackolive":"#3B3C36","blackshadows":"#BFAFB2","blanchedalmond":"#FFEBCD","blast-offbronze":"#A57164","bleudefrance":"#318CE7","blizzardblue":"#ACE5EE","bloodred":"#660000","blue":"#0000FF","blue(crayola)":"#1F75FE","blue(munsell)":"#0093AF","blue(ncs)":"#0087BD","blue(pantone)":"#0018A8","blue(pigment)":"#333399","bluebell":"#A2A2D0","blue-gray(crayola)":"#6699CC","bluejeans":"#5DADEC","bluesapphire":"#126180","blue-violet":"#8A2BE2","blueyonder":"#5072A7","bluetiful":"#3C69E7","blush":"#DE5D83","bole":"#79443B","bone":"#E3DAC9","brickred":"#CB4154","brightlilac":"#D891EF","brightyellow(crayola)":"#FFAA1D","bronze":"#CD7F32","brownsugar":"#AF6E4D","budgreen":"#7BB661","buff":"#FFC680","burgundy":"#800020","burlywood":"#DEB887","burnishedbrown":"#A17A74","burntorange":"#CC5500","burntsienna":"#E97451","burntumber":"#8A3324","byzantine":"#BD33A4","byzantium":"#702963","cadetblue":"#5F9EA0","cadetgrey":"#91A3B0","cadmiumgreen":"#006B3C","cadmiumorange":"#ED872D","caféaulait":"#A67B5B","cafénoir":"#4B3621","cambridgeblue":"#A3C1AD","camel":"#C19A6B","cameopink":"#EFBBCC","canary":"#FFFF99","canaryyellow":"#FFEF00","candypink":"#E4717A","cardinal":"#C41E3A","caribbeangreen":"#00CC99","carmine":"#960018","carmine(m&p)":"#D70040","carnationpink":"#FFA6C9","carnelian":"#B31B1B","carolinablue":"#56A0D3","carrotorange":"#ED9121","catawba":"#703642","cedarchest":"#C95A49","celadon":"#ACE1AF","celeste":"#B2FFFF","cerise":"#DE3163","cerulean":"#007BA7","ceruleanblue":"#2A52BE","ceruleanfrost":"#6D9BC3","cerulean(crayola)":"#1DACD6","champagne":"#F7E7CE","champagnepink":"#F1DDCF","charcoal":"#36454F","charmpink":"#E68FAC","chartreuse(web)":"#80FF00","cherryblossompink":"#FFB7C5","chestnut":"#954535","chilired":"#E23D28","chinapink":"#DE6FA1","chinesered":"#AA381E","chineseviolet":"#856088","chineseyellow":"#FFB200","chocolate(traditional)":"#7B3F00","chocolate(web)":"#D2691E","cinereous":"#98817B","cinnabar":"#E34234","cinnamonsatin":"#CD607E","citrine":"#E4D00A","citron":"#9FA91F","claret":"#7F1734","coffee":"#6F4E37","columbiablue":"#B9D9EB","congopink":"#F88379","coolgrey":"#8C92AC","copper":"#B87333","copper(crayola)":"#DA8A67","copperpenny":"#AD6F69","copperred":"#CB6D51","copperrose":"#996666","coquelicot":"#FF3800","coral":"#FF7F50","coralpink":"#F88379","cordovan":"#893F45","corn":"#FBEC5D","cornflowerblue":"#6495ED","cornsilk":"#FFF8DC","cosmiccobalt":"#2E2D88","cosmiclatte":"#FFF8E7","coyotebrown":"#81613C","cottoncandy":"#FFBCD9","cream":"#FFFDD0","crimson":"#DC143C","crimson(ua)":"#9E1B32","culturedpearl":"#F5F5F5","cyan":"#00FFFF","cyan(process)":"#00B7EB","cybergrape":"#58427C","cyberyellow":"#FFD300","cyclamen":"#F56FA1","darkbrown":"#654321","darkbyzantium":"#5D3954","darkcyan":"#008B8B","darkelectricblue":"#536878","darkgoldenrod":"#B8860B","darkgreen(x11)":"#006400","darkjunglegreen":"#1A2421","darkkhaki":"#BDB76B","darklava":"#483C32","darkliver(horses)":"#543D37","darkmagenta":"#8B008B","darkolivegreen":"#556B2F","darkorange":"#FF8C00","darkorchid":"#9932CC","darkpurple":"#301934","darkred":"#8B0000","darksalmon":"#E9967A","darkseagreen":"#8FBC8F","darksienna":"#3C1414","darkskyblue":"#8CBED6","darkslateblue":"#483D8B","darkslategray":"#2F4F4F","darkspringgreen":"#177245","darkturquoise":"#00CED1","darkviolet":"#9400D3","davy'sgrey":"#555555","deepcerise":"#DA3287","deepchampagne":"#FAD6A5","deepchestnut":"#B94E48","deepjunglegreen":"#004B49","deeppink":"#FF1493","deepsaffron":"#FF9933","deepskyblue":"#00BFFF","deepspacesparkle":"#4A646C","deeptaupe":"#7E5E60","denim":"#1560BD","denimblue":"#2243B6","desert":"#C19A6B","desertsand":"#EDC9AF","dimgray":"#696969","dodgerblue":"#1E90FF","drabdarkbrown":"#4A412A","dukeblue":"#00009C","dutchwhite":"#EFDFBB","ebony":"#555D50","ecru":"#C2B280","eerieblack":"#1B1B1B","eggplant":"#614051","eggshell":"#F0EAD6","electriclime":"#CCFF00","electricpurple":"#BF00FF","electricviolet":"#8F00FF","emerald":"#50C878","eminence":"#6C3082","englishlavender":"#B48395","englishred":"#AB4B52","englishvermillion":"#CC474B","englishviolet":"#563C5C","erin":"#00FF40","etonblue":"#96C8A2","fallow":"#C19A6B","falured":"#801818","fandango":"#B53389","fandangopink":"#DE5285","fawn":"#E5AA70","ferngreen":"#4F7942","fielddrab":"#6C541E","fieryrose":"#FF5470","finn":"#683068","firebrick":"#B22222","fireenginered":"#CE2029","flame":"#E25822","flax":"#EEDC82","flirt":"#A2006D","floralwhite":"#FFFAF0","forestgreen(web)":"#228B22","frenchbeige":"#A67B5B","frenchbistre":"#856D4D","frenchblue":"#0072BB","frenchfuchsia":"#FD3F92","frenchlilac":"#86608E","frenchlime":"#9EFD38","frenchmauve":"#D473D4","frenchpink":"#FD6C9E","frenchraspberry":"#C72C48","frenchskyblue":"#77B5FE","frenchviolet":"#8806CE","frostbite":"#E936A7","fuchsia":"#FF00FF","fuchsia(crayola)":"#C154C1","fulvous":"#E48400","fuzzywuzzy":"#87421F","gainsboro":"#DCDCDC","gamboge":"#E49B0F","genericviridian":"#007F66","ghostwhite":"#F8F8FF","glaucous":"#6082B6","glossygrape":"#AB92B3","gogreen":"#00AB66","gold(metallic)":"#D4AF37","gold(web)(golden)":"#FFD700","gold(crayola)":"#E6BE8A","goldfusion":"#85754E","goldenbrown":"#996515","goldenpoppy":"#FCC200","goldenyellow":"#FFDF00","goldenrod":"#DAA520","gothamgreen":"#00573F","granitegray":"#676767","grannysmithapple":"#A8E4A0","gray(web)":"#808080","gray(x11gray)":"#BEBEBE","green":"#00FF00","green(crayola)":"#1CAC78","green(web)":"#008000","green(munsell)":"#00A877","green(ncs)":"#009F6B","green(pantone)":"#00AD43","green(pigment)":"#00A550","green-blue":"#1164B4","greenlizard":"#A7F432","greensheen":"#6EAEA1","gunmetal":"#2a3439","hansayellow":"#E9D66B","harlequin":"#3FFF00","harvestgold":"#DA9100","heatwave":"#FF7A00","heliotrope":"#DF73FF","heliotropegray":"#AA98A9","hollywoodcerise":"#F400A1","honolulublue":"#006DB0","hooker'sgreen":"#49796B","hotmagenta":"#FF1DCE","hotpink":"#FF69B4","huntergreen":"#355E3B","iceberg":"#71A6D2","illuminatingemerald":"#319177","imperialred":"#ED2939","inchworm":"#B2EC5D","independence":"#4C516D","indiagreen":"#138808","indianred":"#CD5C5C","indianyellow":"#E3A857","indigo":"#4B0082","indigodye":"#00416A","internationalkleinblue":"#130a8f","internationalorange(engineering)":"#BA160C","internationalorange(goldengatebridge)":"#C0362C","irresistible":"#B3446C","isabelline":"#F4F0EC","italianskyblue":"#B2FFFF","ivory":"#FFFFF0","japanesecarmine":"#9D2933","japaneseviolet":"#5B3256","jasmine":"#F8DE7E","jazzberryjam":"#A50B5E","jet":"#343434","jonquil":"#F4CA16","junebud":"#BDDA57","junglegreen":"#29AB87","kellygreen":"#4CBB17","keppel":"#3AB09E","keylime":"#E8F48C","khaki(web)":"#C3B091","khaki(x11)(lightkhaki)":"#F0E68C","kobe":"#882D17","kobi":"#E79FC4","kobicha":"#6B4423","ksupurple":"#512888","languidlavender":"#D6CADD","lapislazuli":"#26619C","laserlemon":"#FFFF66","laurelgreen":"#A9BA9D","lava":"#CF1020","lavender(floral)":"#B57EDC","lavender(web)":"#E6E6FA","lavenderblue":"#CCCCFF","lavenderblush":"#FFF0F5","lavendergray":"#C4C3D0","lawngreen":"#7CFC00","lemon":"#FFF700","lemonchiffon":"#FFFACD","lemoncurry":"#CCA01D","lemonglacier":"#FDFF00","lemonmeringue":"#F6EABE","lemonyellow":"#FFF44F","lemonyellow(crayola)":"#FFFF9F","liberty":"#545AA7","lightblue":"#ADD8E6","lightcoral":"#F08080","lightcornflowerblue":"#93CCEA","lightcyan":"#E0FFFF","lightfrenchbeige":"#C8AD7F","lightgoldenrodyellow":"#FAFAD2","lightgray":"#D3D3D3","lightgreen":"#90EE90","lightorange":"#FED8B1","lightperiwinkle":"#C5CBE1","lightpink":"#FFB6C1","lightsalmon":"#FFA07A","lightseagreen":"#20B2AA","lightskyblue":"#87CEFA","lightslategray":"#778899","lightsteelblue":"#B0C4DE","lightyellow":"#FFFFE0","lilac":"#C8A2C8","lilacluster":"#AE98AA","lime(colorwheel)":"#BFFF00","lime(web)(x11green)":"#00FF00","limegreen":"#32CD32","lincolngreen":"#195905","linen":"#FAF0E6","lion":"#DECC9C","liseranpurple":"#DE6FA1","littleboyblue":"#6CA0DC","liver":"#674C47","liver(dogs)":"#B86D29","liver(organ)":"#6C2E1F","liverchestnut":"#987456","livid":"#6699CC","macaroniandcheese":"#FFBD88","madderlake":"#CC3336","magenta":"#FF00FF","magenta(crayola)":"#F653A6","magenta(dye)":"#CA1F7B","magenta(pantone)":"#D0417E","magenta(process)":"#FF0090","magentahaze":"#9F4576","magicmint":"#AAF0D1","magnolia":"#F2E8D7","mahogany":"#C04000","maize":"#FBEC5D","maize(crayola)":"#F2C649","majorelleblue":"#6050DC","malachite":"#0BDA51","manatee":"#979AAA","mandarin":"#F37A48","mango":"#FDBE02","mangotango":"#FF8243","mantis":"#74C365","mardigras":"#880085","marigold":"#EAA221","maroon(crayola)":"#C32148","maroon":"#800000","maroon(x11)":"#B03060","mauve":"#E0B0FF","mauvetaupe":"#915F6D","mauvelous":"#EF98AA","maximumblue":"#47ABCC","maximumbluegreen":"#30BFBF","maximumbluepurple":"#ACACE6","maximumgreen":"#5E8C31","maximumgreenyellow":"#D9E650","maximumpurple":"#733380","maximumred":"#D92121","maximumredpurple":"#A63A79","maximumyellow":"#FAFA37","maximumyellowred":"#F2BA49","maygreen":"#4C9141","mayablue":"#73C2FB","mediumaquamarine":"#66DDAA","mediumblue":"#0000CD","mediumcandyapplered":"#E2062C","mediumcarmine":"#AF4035","mediumchampagne":"#F3E5AB","mediumorchid":"#BA55D3","mediumpurple":"#9370DB","mediumseagreen":"#3CB371","mediumslateblue":"#7B68EE","mediumspringgreen":"#00FA9A","mediumturquoise":"#48D1CC","mediumviolet-red":"#C71585","mellowapricot":"#F8B878","mellowyellow":"#F8DE7E","melon":"#FEBAAD","metallicgold":"#D3AF37","metallicseaweed":"#0A7E8C","metallicsunburst":"#9C7C38","mexicanpink":"#E4007C","middleblue":"#7ED4E6","middlebluegreen":"#8DD9CC","middlebluepurple":"#8B72BE","middlegrey":"#8B8680","middlegreen":"#4D8C57","middlegreenyellow":"#ACBF60","middlepurple":"#D982B5","middlered":"#E58E73","middleredpurple":"#A55353","middleyellow":"#FFEB00","middleyellowred":"#ECB176","midnight":"#702670","midnightblue":"#191970","midnightgreen(eaglegreen)":"#004953","mikadoyellow":"#FFC40C","mimipink":"#FFDAE9","mindaro":"#E3F988","ming":"#36747D","minionyellow":"#F5E050","mint":"#3EB489","mintcream":"#F5FFFA","mintgreen":"#98FF98","mistymoss":"#BBB477","mistyrose":"#FFE4E1","modebeige":"#967117","monalisa":"#FF948E","morningblue":"#8DA399","mossgreen":"#8A9A5B","mountainmeadow":"#30BA8F","mountbattenpink":"#997A8D","msugreen":"#18453B","mulberry":"#C54B8C","mulberry(crayola)":"#C8509B","mustard":"#FFDB58","myrtlegreen":"#317873","mystic":"#D65282","mysticmaroon":"#AD4379","nadeshikopink":"#F6ADC6","naplesyellow":"#FADA5E","navajowhite":"#FFDEAD","navyblue":"#000080","navyblue(crayola)":"#1974D2","neonblue":"#4666FF","neongreen":"#39FF14","neonfuchsia":"#FE4164","newyorkpink":"#D7837F","nickel":"#727472","non-photoblue":"#A4DDED","nyanza":"#E9FFDB","ochre":"#CC7722","oldburgundy":"#43302E","oldgold":"#CFB53B","oldlace":"#FDF5E6","oldlavender":"#796878","oldmauve":"#673147","oldrose":"#C08081","oldsilver":"#848482","olive":"#808000","olivedrab(#3)":"#6","olivedrab#7":"#3C","olivegreen":"#B5B35C","olivine":"#9AB973","onyx":"#353839","opal":"#A8C3BC","operamauve":"#B784A7","orange":"#FF7F00","orange(crayola)":"#FF7538","orange(pantone)":"#FF5800","orange(web)":"#FFA500","orangepeel":"#FF9F00","orange-red":"#FF681F","orange-red(crayola)":"#FF5349","orangesoda":"#FA5B3D","orange-yellow":"#F5BD1F","orange-yellow(crayola)":"#F8D568","orchid":"#DA70D6","orchidpink":"#F2BDCD","orchid(crayola)":"#E29CD2","outerspace(crayola)":"#2D383A","outrageousorange":"#FF6E4A","oxblood":"#4A0000","oxfordblue":"#002147","oucrimsonred":"#841617","pacificblue":"#1CA9C9","pakistangreen":"#006600","palatinatepurple":"#682860","paleaqua":"#BED3E5","palecerulean":"#9BC4E2","paledogwood":"#ED7A9B","palepink":"#FADADD","palepurple(pantone)":"#FAE6FA","palespringbud":"#ECEBBD","pansypurple":"#78184A","paoloveronesegreen":"#009B7D","papayawhip":"#FFEFD5","paradisepink":"#E63E62","parchment":"#F1E9D2","parisgreen":"#50C878","pastelpink":"#DEA5A4","patriarch":"#800080","paua":"#1F005E","payne'sgrey":"#536878","peach":"#FFE5B4","peach(crayola)":"#FFCBA4","peachpuff":"#FFDAB9","pear":"#D1E231","pearlypurple":"#B768A2","periwinkle":"#CCCCFF","periwinkle(crayola)":"#C3CDE6","permanentgeraniumlake":"#E12C2C","persianblue":"#1C39BB","persiangreen":"#00A693","persianindigo":"#32127A","persianorange":"#D99058","persianpink":"#F77FBE","persianplum":"#701C1C","persianred":"#CC3333","persianrose":"#FE28A2","persimmon":"#EC5800","pewterblue":"#8BA8B7","phlox":"#DF00FF","phthaloblue":"#000F89","phthalogreen":"#123524","picoteeblue":"#2E2787","pictorialcarmine":"#C30B4E","piggypink":"#FDDDE6","pinegreen":"#01796F","pinetree":"#2A2F23","pink":"#FFC0CB","pink(pantone)":"#D74894","pinklace":"#FFDDF4","pinklavender":"#D8B2D1","pinksherbet":"#F78FA7","pistachio":"#93C572","platinum":"#E5E4E2","plum":"#8E4585","plum(web)":"#DDA0DD","plumppurple":"#5946B2","polishedpine":"#5DA493","pompandpower":"#86608E","popstar":"#BE4F62","portlandorange":"#FF5A36","powderblue":"#B0E0E6","princetonorange":"#F58025","processyellow":"#FFEF00","prune":"#701C1C","prussianblue":"#003153","psychedelicpurple":"#DF00FF","puce":"#CC8899","pullmanbrown(upsbrown)":"#644117","pumpkin":"#FF7518","purple":"#6A0DAD","purple(web)":"#800080","purple(munsell)":"#9F00C5","purple(x11)":"#A020F0","purplemountainmajesty":"#9678B6","purplenavy":"#4E5180","purplepizzazz":"#FE4EDA","purpleplum":"#9C51B6","purpureus":"#9A4EAE","queenblue":"#436B95","queenpink":"#E8CCD7","quicksilver":"#A6A6A6","quinacridonemagenta":"#8E3A59","radicalred":"#FF355E","raisinblack":"#242124","rajah":"#FBAB60","raspberry":"#E30B5D","raspberryglacé":"#915F6D","raspberryrose":"#B3446C","rawsienna":"#D68A59","rawumber":"#826644","razzledazzlerose":"#FF33CC","razzmatazz":"#E3256B","razzmicberry":"#8D4E85","rebeccapurple":"#663399","red":"#FF0000","red(crayola)":"#EE204D","red(munsell)":"#F2003C","red(ncs)":"#C40233","red(pantone)":"#ED2939","red(pigment)":"#ED1C24","red(ryb)":"#FE2712","red-orange":"#FF5349","red-orange(crayola)":"#FF681F","red-orange(colorwheel)":"#FF4500","red-purple":"#E40078","redsalsa":"#FD3A4A","red-violet":"#C71585","red-violet(crayola)":"#C0448F","red-violet(colorwheel)":"#922B3E","redwood":"#A45A52","resolutionblue":"#002387","rhythm":"#777696","richblack":"#004040","richblack(fogra29)":"#010B13","richblack(fogra39)":"#010203","riflegreen":"#444C38","robineggblue":"#00CCCC","rocketmetallic":"#8A7F80","rojospanishred":"#A91101","romansilver":"#838996","rose":"#FF007F","rosebonbon":"#F9429E","rosedust":"#9E5E6F","roseebony":"#674846","rosemadder":"#E32636","rosepink":"#FF66CC","rosepompadour":"#ED7A9B","rosered":"#C21E56","rosetaupe":"#905D5D","rosevale":"#AB4E52","rosewood":"#65000B","rossocorsa":"#D40000","rosybrown":"#BC8F8F","royalblue(dark)":"#002366","royalblue(light)":"#4169E1","royalpurple":"#7851A9","royalyellow":"#FADA5E","ruber":"#CE4676","rubinered":"#D10056","ruby":"#E0115F","rubyred":"#9B111E","rufous":"#A81C07","russet":"#80461B","russiangreen":"#679267","russianviolet":"#32174D","rust":"#B7410E","rustyred":"#DA2C43","sacramentostategreen":"#043927","saddlebrown":"#8B4513","safetyorange":"#FF7800","safetyorange(blazeorange)":"#FF6700","safetyyellow":"#EED202","saffron":"#F4C430","sage":"#BCB88A","st.patrick'sblue":"#23297A","salmon":"#FA8072","salmonpink":"#FF91A4","sand":"#C2B280","sanddune":"#967117","sandybrown":"#F4A460","sapgreen":"#507D2A","sapphire":"#0F52BA","sapphireblue":"#0067A5","sapphire(crayola)":"#2D5DA1","satinsheengold":"#CBA135","scarlet":"#FF2400","schausspink":"#FF91AF","schoolbusyellow":"#FFD800","screamin'green":"#66FF66","seagreen":"#2E8B57","seagreen(crayola)":"#00FFCD","seance":"#612086","sealbrown":"#59260B","seashell":"#FFF5EE","secret":"#764374","selectiveyellow":"#FFBA00","sepia":"#704214","shadow":"#8A795D","shadowblue":"#778BA5","shamrockgreen":"#009E60","sheengreen":"#8FD400","shimmeringblush":"#D98695","shinyshamrock":"#5FA778","shockingpink":"#FC0FC0","shockingpink(crayola)":"#FF6FFF","sienna":"#882D17","silver":"#C0C0C0","silver(crayola)":"#C9C0BB","silver(metallic)":"#AAA9AD","silverchalice":"#ACACAC","silverpink":"#C4AEAD","silversand":"#BFC1C2","sinopia":"#CB410B","sizzlingred":"#FF3855","sizzlingsunrise":"#FFDB00","skobeloff":"#007474","skyblue":"#87CEEB","skyblue(crayola)":"#76D7EA","skymagenta":"#CF71AF","slateblue":"#6A5ACD","slategray":"#708090","slimygreen":"#299617","smitten":"#C84186","smokyblack":"#100C08","snow":"#FFFAFA","solidpink":"#893843","sonicsilver":"#757575","spacecadet":"#1D2951","spanishbistre":"#807532","spanishblue":"#0070B8","spanishcarmine":"#D10047","spanishgray":"#989898","spanishgreen":"#009150","spanishorange":"#E86100","spanishpink":"#F7BFBE","spanishred":"#E60026","spanishskyblue":"#00FFFE","spanishviolet":"#4C2882","spanishviridian":"#007F5C","springbud":"#A7FC00","springfrost":"#87FF2A","springgreen":"#00FF7F","springgreen(crayola)":"#ECEBBD","starcommandblue":"#007BB8","steelblue":"#4682B4","steelpink":"#CC33CC","stildegrainyellow":"#FADA5E","straw":"#E4D96F","strawberry":"#FA5053","strawberryblonde":"#FF9361","stronglimegreen":"#33CC33","sugarplum":"#914E75","sunglow":"#FFCC33","sunray":"#E3AB57","sunset":"#FAD6A5","superpink":"#CF6BA9","sweetbrown":"#A83731","syracuseorange":"#D44500","tan":"#D2B48C","tan(crayola)":"#D99A6C","tangerine":"#F28500","tangopink":"#E4717A","tartorange":"#FB4D46","taupe":"#483C32","taupegray":"#8B8589","teagreen":"#D0F0C0","tearose":"#F4C2C2","teal":"#008080","tealblue":"#367588","telemagenta":"#CF3476","tenné(tawny)":"#CD5700","terracotta":"#E2725B","thistle":"#D8BFD8","thulianpink":"#DE6FA1","ticklemepink":"#FC89AC","tiffanyblue":"#0ABAB5","timberwolf":"#DBD7D2","titaniumyellow":"#EEE600","tomato":"#FF6347","tourmaline":"#86A1A9","tropicalrainforest":"#00755E","trueblue":"#2D68C4","trypanblue":"#1C05B3","tuftsblue":"#3E8EDE","tumbleweed":"#DEAA88","turquoise":"#40E0D0","turquoiseblue":"#00FFEF","turquoisegreen":"#A0D6B4","turtlegreen":"#8A9A5B","tuscan":"#FAD6A5","tuscanbrown":"#6F4E37","tuscanred":"#7C4848","tuscantan":"#A67B5B","tuscany":"#C09999","twilightlavender":"#8A496B","tyrianpurple":"#66023C","uablue":"#0033AA","uared":"#D9004C","ultramarine":"#3F00FF","ultramarineblue":"#4166F5","ultrapink":"#FF6FFF","ultrared":"#FC6C85","umber":"#635147","unbleachedsilk":"#FFDDCA","unitednationsblue":"#5B92E5","universityofpennsylvaniared":"#A50021","unmellowyellow":"#FFFF66","upforestgreen":"#014421","upmaroon":"#7B1113","upsdellred":"#AE2029","uranianblue":"#AFDBF5","usafablue":"#004F98","vandykebrown":"#664228","vanilla":"#F3E5AB","vanillaice":"#F38FA9","vegasgold":"#C5B358","venetianred":"#C80815","verdigris":"#43B3AE","vermilion":"#E34234","vermilion":"#D9381E","veronica":"#A020F0","violet":"#8F00FF","violet(colorwheel)":"#7F00FF","violet(crayola)":"#963D7F","violet(ryb)":"#8601AF","violet(web)":"#EE82EE","violet-blue":"#324AB2","violet-blue(crayola)":"#766EC8","violet-red":"#F75394","violet-red(perbang)":"#F0599C","viridian":"#40826D","viridiangreen":"#009698","vividburgundy":"#9F1D35","vividskyblue":"#00CCFF","vividtangerine":"#FFA089","vividviolet":"#9F00FF","volt":"#CEFF00","warmblack":"#004242","weezyblue":"#189BCC","wheat":"#F5DEB3","white":"#FFFFFF","wildblueyonder":"#A2ADD0","wildorchid":"#D470A2","wildstrawberry":"#FF43A4","wildwatermelon":"#FC6C85","windsortan":"#A75502","wine":"#722F37","winedregs":"#673147","wintersky":"#FF007C","wintergreendream":"#56887D","wisteria":"#C9A0DC","woodbrown":"#C19A6B","xanadu":"#738678","xanthic":"#EEED09","xanthous":"#F1B42F","yaleblue":"#00356B","yellow":"#FFFF00","yellow(crayola)":"#FCE883","yellow(munsell)":"#EFCC00","yellow(ncs)":"#FFD300","yellow(pantone)":"#FEDF00","yellow(process)":"#FFEF00","yellow(ryb)":"#FEFE33","yellow-green":"#9ACD32","yellow-green(crayola)":"#C5E384","yellow-green(colorwheel)":"#30B21A","yelloworange":"#FFAE42","yelloworange(colorwheel)":"#FF9505","yellowsunshine":"#FFF700","yinmnblue":"#2E5090","zaffre":"#0014A8","zomp":"#39A78E","grey":"#808080","brown":"#654320","lime":"2AFF00"}

def index(request):
    return render(request,'mainpage.html')

def chat(request):
    removeOldChats()
    removeOldUsers()
    removeUnusedServers()

    #Getting data from page
    try:
        name = request.POST["name"]
        room = request.POST["room"]
        pw = request.POST["password"]
    except:
        return HttpResponseRedirect(reverse('index'))
    
    #Pre-fetch validation
    name = name.strip()
    if name=='' or room=='':
        messages.success(request,"Error: Empty string")
        return HttpResponseRedirect(reverse('index'))
    elif name.lower().strip()=='admin':
        messages.success(request,"Error: Invalid name")
        return HttpResponseRedirect(reverse('index'))
    elif len(name) > 16:
        messages.success(request,"Error: Name too long")
        return HttpResponseRedirect(reverse('index'))
    elif len(room) > 16:
        messages.success(request,"Error: Room name too long")
        return HttpResponseRedirect(reverse('index'))

    else:

        #Get server
        try:
            serv = ServerList.objects.get(server=room)
        except:
            serv = None

        #If server doesn't exist, create it
        if serv==None:
            s = ServerList(server=room,lockStatus=False,lastUpdate=datetime.datetime.now().astimezone(),password='none')
            s.save()

            #Add user to server
            u = UserList(username=name,server=s,time=datetime.datetime.now().astimezone())
            u.save()

            #Show that user joined
            c = Chats(server=s,username='admin',message=f"Room '{room}' created.",time=datetime.datetime.now().astimezone())
            c.save()
            c = Chats(server=s,username='admin',message=f"{name} joined the chat.",time=datetime.datetime.now().astimezone())
            c.save()

        else:
            #if server is locked, deny
            if serv.lockStatus==True:
                
                #if password needed
                if serv.password!='none':
                    if serv.password!=pw:
                        messages.success(request,"Error: Password needed")
                        return HttpResponseRedirect(reverse('index'))
                else:
                    messages.success(request,"Error: Room is locked")
                    return HttpResponseRedirect(reverse('index'))

            #if user in server, deny
            try:
                u = UserList.objects.get(server=serv,username=name)
            except:
                u = None
            if u!=None:
                messages.success(request,"Error: Name in use for server")
                return HttpResponseRedirect(reverse('index'))
            
            #Add user to server
            u = UserList(username=name,server=serv,time=datetime.datetime.now().astimezone())
            u.save()
            #Show that user joined
            c = Chats(server=serv,username='admin',message=f"{name} joined the chat.",time=datetime.datetime.now().astimezone())
            c.save()
            
            #Validation done, ready to connect
        c = {
            "room":room,
            "name":name,
        }
        return render(request,'chatpage.html',context=c)   

def sendmsg(request):

    #default fetch method
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request)
        msg = data_from_post.get("message")
        room = data_from_post.get("room")
        name = data_from_post.get("name")

        #validate message
        if len(msg) > 0 and len(msg) < 100000:

            #add message as chat and update server last message
            time = datetime.datetime.now().astimezone()
            serv = ServerList.objects.filter(server=room)[0]
            c = Chats(server=serv,username=name,message=msg,time=time)
            c.save()
            UserList.objects.filter(server=room,username=name).update(time=time)
            ServerList.objects.filter(server=room).update(lastUpdate=time)

            removeOldChats()
            removeOldUsers()
            removeUnusedServers()

        return JsonResponse({})  

def sendcmd(request):

    #default fetch method
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        js = json.load(request)
        
        command = js.get("command").strip().lower()
        serv = js.get("room")
        
        #if leave, send redirect command
        if command=="leave":
            return JsonResponse({'response':'home'})

        #if unlock, set room status as unlocked and output chat message saying server is unlocked
        elif command=="unlock":
            s = ServerList.objects.get(server=serv)
            if s.lockStatus==True:
                ServerList.objects.filter(server=serv).update(lockStatus=False)
                c = Chats(server=ServerList.objects.get(server=serv),username='admin',message="Server unlocked.",time=datetime.datetime.now().astimezone())
                c.save()
            return JsonResponse({})
        
        #If close, remove all users, messages, server and redirect user. 
        elif command=="close":
            removeOldUsers()
            
            #only close if 1 user in it
            u = UserList.objects.filter(server=serv).values()
            if len(u)==1:
                s = ServerList.objects.get(server=serv)
                for i in Chats.objects.filter(server=s).values():
                    chatID = i.get("chatID")
                    c = Chats.objects.get(chatID=chatID)
                    c.delete()
                s.delete()
                return JsonResponse({'response':'home'})
            else:
                c = Chats(server=ServerList.objects.get(server=serv),username='admin',message="Chatroom could not be closed.",time=datetime.datetime.now().astimezone())
                c.save()
            return JsonResponse({})

        command=command.split(" ")

        #if lock, find if password is present in message, update server, send output to chat
        if command[0]=='lock':
            
            #no password
            if len(command)==1:
                s = ServerList.objects.get(server=serv)
                if s.lockStatus==False:
                    ServerList.objects.filter(server=serv).update(lockStatus=True,password="none")
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message="Server locked.",time=datetime.datetime.now().astimezone())
                    c.save()
                
            else:

                #password
                pw = command[1]
                if len(pw)>16:
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message=f"Server password too long.",time=datetime.datetime.now().astimezone())
                    c.save()
                
                #if password = current password, do nothing
                elif pw!=ServerList.objects.get(server=serv).password:
                    ServerList.objects.filter(server=serv).update(lockStatus=True,password=pw)
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message=f"Server password set: {pw}",time=datetime.datetime.now().astimezone())
                    c.save()
            
            return JsonResponse({})

        #If colour, validate colour then send message to server, which will update page
        elif command[0] == 'color' or command[0] == 'colour' or command[0] == 'fg':

            #get color
            if len(command)==2:
                color = command[1]
                v = True
                if color.lower() in color_dict:
                    color = color_dict[color.lower()]
                elif len(color) == 7:
                    if color[0] != '#':
                        v = False
                    for i,c in enumerate(color):
                        if c not in '0123456789ABCDEFabcdef' and i>0:
                            v = False
                elif len(color) == 6:
                    for c in color:
                        if c not in '0123456789ABCDEFabcdef':
                            v = False
                    color = '#' + color
                else:
                    v = False
                if v:
                    color = color.upper()
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message=f"Text color changed to {color}.",time=datetime.datetime.now().astimezone())
                    c.save()
        
        #If background, validate colour then send message to server, which will update page
        elif command[0] == 'background' or command[0] == 'bg':
            #get color
            if len(command)==2:
                color = command[1]
                v = True
                if color.lower() in color_dict:
                    color = color_dict[color.lower()]
                elif len(color) == 7:
                    if color[0] != '#':
                        v = False
                    for i,c in enumerate(color):
                        if c not in '0123456789ABCDEFabcdef' and i>0:
                            v = False
                elif len(color) == 6:
                    for c in color:
                        if c not in '0123456789ABCDEFabcdef':
                            v = False
                    color = '#' + color
                else:
                    v = False
                if v:
                    color = color.upper()
                    c = Chats(server=ServerList.objects.get(server=serv),username='admin',message=f"Background color changed to {color}.",time=datetime.datetime.now().astimezone())
                    c.save()


        return JsonResponse({})

def getchats(request):

    #default fetch request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request) #Get data from POST request
        room = data_from_post["room"]
        name = data_from_post["name"]
        last = data_from_post["last"]

        #check if user already exists
        u = UserList.objects.filter(server=room,username=name)
        if len(u.values())==0:

            #re-add user
            u = UserList(username=name,server=ServerList.objects.get(server=room),time=datetime.datetime.now().astimezone())
            u.save()

            #show that user joined
            c = Chats(server=ServerList.objects.get(server=room),username='admin',message=f"{name} joined the chat.",time=datetime.datetime.now().astimezone())
            c.save()

        else:
            #update user
            u.update(time=datetime.datetime.now().astimezone())

        #return chats since last update
        data = {}
        for i in Chats.objects.filter(server=room).order_by('time').values():
            if i["chatID"] > int(last):
                time = str(i["time"]).split(" ")[1].split(".")[0]
                data[i["chatID"]] = [i["username"],i["message"],time]
                last = i["chatID"]
        data["last"] = last
        return JsonResponse(data)  

def removeOldUsers():

    #Updating users from server
    for i in UserList.objects.all().order_by('time').values():
        id = i.get('userID')
        name = i.get('username')
        time = i.get('time')
        serv = ServerList.objects.get(server=i.get('server_id'))
        timeout = datetime.datetime.now().astimezone() - datetime.timedelta(seconds=15)

        #remove all users where timeout has occurred
        if time <= timeout:
            UserList.objects.filter(userID=id).delete()

            #Show that user left
            c = Chats(server=serv,username='admin',message=f"{name} left the chat.",time=datetime.datetime.now().astimezone())
            c.save()
        else:
            break

def removeOldChats():
    #removing items over 1d old
    for i in Chats.objects.all().order_by('time').values():
        id = i.get("chatID")
        time = i.get("time")
        yesterday = datetime.datetime.now().astimezone() - datetime.timedelta(days=1)

        #remove all chats where timeout has occurred
        if time <= yesterday:
            Chats.objects.filter(chatID=id).delete()
        else:
            break

def removeUnusedServers():
    for i in ServerList.objects.all().order_by('lastUpdate').values():
        id = i.get("server")
        time = i.get("lastUpdate")
        lock = i.get("lockStatus")
        server = ServerList.objects.get(server=id)
        t = datetime.datetime.now().astimezone() - datetime.timedelta(hours=1)
        chats = Chats.objects.filter(server=server).values()
        users = UserList.objects.filter(server=server).values()

        #remove all servers where timeout has occurred
        if time <= t and len(chats)==0 and len(users)==0:
            server.delete()

        elif len(users)==0 and lock==True:

            #delete all msgs
            for j in Chats.objects.filter(server=server).values():
                chatID = j.get("chatID")
                c = Chats.objects.get(chatID=chatID)
                c.delete()
            server.delete()
            
def getusers(request):
    removeOldUsers()

    #fetch command
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data_from_post = json.load(request)
        room = data_from_post["room"]

        #get number of users in server
        data = {'user_num':len(UserList.objects.filter(server=ServerList.objects.get(server=room)).values())}
        return JsonResponse(data)

