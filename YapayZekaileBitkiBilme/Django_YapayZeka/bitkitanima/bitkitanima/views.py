
from tensorflow.keras.applications.vgg16 import preprocess_input
from PIL import Image 
import numpy as np
import os
from keras.models import load_model
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

class Flower:
    def __init__(self, name, habitat, color, characteristics):
        self.name = name
        self.habitat = habitat
        self.color = color
        self.characteristics = characteristics

    def display_info(self):
        print(f"Çiçek Adı: {self.name}")
        print(f"Yetiştiği Yer: {self.habitat}")
        print(f"Rengi: {self.color}")
        print("Genel Özellikleri:")
        for char in self.characteristics:
            print(f" - {char}")

flowers_list = []
AlpineSeaHolly = Flower(
    name="Alpine Sea Holly (Alp Deniz Değirmeni)",
    habitat="Avrupa'ya özgü olan Alp Deniz Değirmeni, dağlık bölgelerde yetişir.",
    color="Mavi tonlarına sahip olan Alp Deniz Değirmeni'nin çiçekleri genellikle mavi renktedir.",
    characteristics="Alp Deniz Değirmeni, denizde yetişen yabanıl bir bitki olan deniz değirmeni ile benzer bir görünüme sahiptir. Thistle ailesine ait olan bu bitki, dik ve sivri yapraklara sahiptir. Çiçekleri çoğunlukla mavi renkte olup, bazen beyaz veya pembe renkli türleri de bulunabilir. Dikenli ve bozuk topraklarda yetişmeye uygundur. Peyzaj düzenlemelerinde süs bitkisi olarak da kullanılır."
)
Anthurium=Flower(
    name="Anthurium",
    habitat="Anthurium bitkisi, tropikal bölgelerde, özellikle Orta ve Güney Amerika'da doğal olarak yetişir.",
    color="Anthurium çiçekleri genellikle kırmızı, pembemsi veya beyaz renklerde olabilir. Ancak farklı türleri farklı renklerde çiçeklere sahip olabilir.",
    characteristics="Anthurium bitkisi, parlak ve dayanıklı yaprakları ve çarpıcı çiçekleri ile bilinir. Çiçeklerin kendine özgü görünümü, uzun ve kalın bir sapın üzerinde yer alır. Her çiçek, genellikle parlak ve ışıltılı bir yaprakla çevrilidir, bu yaprak gerçek çiçeği korur ve renkli bir yaprak olarak görünür. Anthurium bitkisi iç mekan bitkisi olarak yetiştirilebilir ve dekoratif bir etki yaratır."
)
Artichoke=Flower(
    name="Artichoke (Enginar)",
    habitat="Akdeniz bölgesi, özellikle İtalya, Fransa ve İspanya gibi ülkelerde yetişir.",
    color="Enginarın mor-mavi renkte ve yeşil-kahverengi tonlarda çeşitleri bulunur.",
    characteristics="Enginar, dikenli bir bitki olan enginar bitkisinin çiçek tomurcuğunun yenilebilir kısmıdır. Yemeklik olarak kullanılan bu bitkinin tomurcuğu, pişirildiğinde yumuşak ve lezzetli bir iç yapısına sahiptir. Yemeklerde veya salatalarda kullanılabilir. Ayrıca enginarın sağlık açısından da birçok faydası bulunmaktadır."
)
Azalea=Flower(
    name="Azalea",
    habitat="Asya ve Kuzey Amerika bölgelerinde yetişen Azalea çiçeği, genellikle nemli ve gölgeli alanlarda bulunur.",
    color="Azalea çiçekleri çeşitli renklerde olabilir, örneğin pembe, beyaz, kırmızı, mor gibi renk tonlarına sahip çeşitleri mevcuttur.",
    characteristics=" Azalea, parlak ve renkli çiçekleri ile bilinen bir çalı türüdür. Gösterişli çiçekleri ve dekoratif yaprakları sayesinde bahçelerde ve parklarda sıkça kullanılır. Genellikle yapraklarının alt tarafı tüylüdür. Azalealar, toprak pH'sına duyarlıdır ve hafif asidik topraklarda daha iyi gelişirler."
)
BallMoss=Flower(
    name="Ball Moss",
    habitat="Ball Moss, genellikle Amerika Birleşik Devletleri'nin güney bölgelerinde, Orta Amerika ve Güney Amerika'da yaygın olarak bulunan bir epifit türüdür. Ağaç dalları, teller veya teller üzerinde asılı olarak yaşar.",
    color="Ball Moss'un renkleri genellikle yeşilimsi gruptan başlayarak griye doğru değişebilir.",
    characteristics="Ball Moss, asalak olmayan bir epifittir, yani ağaçlara zarar vermez veya onlardan beslenmez. Nemli ve nemli alanlarda bulunurlar ve genellikle diğer bitkilerin dallarına asılı olarak büyürler. Küçük bir topluluk oluşturarak gruplar halinde görülebilirler. Ball Moss, dallara yapışan toplulukları oluşturarak dekoratif bir görünüm sunabilir."
)
BalloonFlower=Flower(
    name="Balloon Flower (Balon Çiçeği)",
    habitat="Balon çiçeği, Asya'nın doğu bölgelerine özgüdür. Japonya, Çin ve Kore gibi bölgelerde doğal olarak yetişir.",
    color="Balon çiçeği çeşitli renklere sahip olabilir, genellikle mavi, beyaz, pembe veya mor tonlarına sahiptir.",
    characteristics="Balon çiçeği, benzersiz açılır ve şişen çiçek tomurcuklarıyla tanınır. Bu tomurcuklar açıldığında çiçekler, bir balonun şişmesine benzeyen bir şekil alır. Bitkinin yaprakları da zarif ve oval şekildedir. Balon çiçeği, bahar ve yaz aylarında çiçek açar ve bahçelerde, saksılarda veya kesme çiçek olarak kullanım için popüler bir seçenektir. Ayrıca uzun ömürlü bir çiçektir, böylece çiçeklenme dönemi boyunca uzun süre sürebilir."
)
BarbetonDaisy=Flower(
    name="Barbeton Daisy (Barberton papatyası)",
    habitat="Barbeton Daisy, Güney Afrika'ya özgü bir çiçek türüdür.",
    color="Beyaz veya pembe renkte olabilir.",
    characteristics="Barbeton Daisy, Asteraceae familyasına ait olan ve genellikle beyaz veya pembe renkte çiçekleri olan bir bitkidir. Bu çiçeğin çiçekleri genellikle tepe noktasında yer alır ve yaygın olarak bahçe süslemelerinde kullanılır. Barbeton Daisy, iyi bir güneş ışığı alan bölgelerde yetişir ve kuraklığa dayanıklıdır. Bitkinin hoş kokusu ve rengarenk çiçekleri, bahçe peyzajında güzel bir görüntü oluşturmak için tercih edilir."
)
BeardedIris=Flower(
    name="Bearded Iris (Alman Süseni)",
    habitat="Kuzey Amerika, Avrupa ve Asya'nın çeşitli bölgeleri.",
    color="Genellikle mavi, mor, beyaz, sarı ve rengarenk çeşitli renklerde olabilir.",
    characteristics="Bearded Iris, soğanlı ve rizomlu bir bitki türüdür. İris ailesine aittir. 'Sakallı' adını taşımasının nedeni, çiçeklerin alt dudaklarının kenarlarında bulunan ve sakalı andıran uzantılardır. Çiçekleri büyük ve gösterişlidir. İrisler genellikle bahçe süslemeleri için tercih edilir. Farklı renk seçenekleri ve çiçek şekilleri ile dikkat çekerler. Farklı türleri ve çeşitleri vardır."
)
BeeBalm=Flower(
    name="Bee Balm (Monarda)",
    habitat="Kuzey Amerika'da doğal olarak yetişen bir bitki türüdür.",
    color="Kırmızı, pembe, mor veya beyaz gibi farklı renk tonlarında çiçeklere sahip olabilir.",
    characteristics=" Bee Balm, tıbbi ve aromatik özellikleri nedeniyle bahçelerde yetiştirilen popüler bir bitki türüdür. Hem estetik hem de pratik kullanımları vardır. Çiçekler, arılar gibi böcekleri cezbetme yetenekleriyle bilinir ve bu nedenle 'Bee Balm' adını almıştır. Bitkinin yaprakları ve çiçekleri hoş bir nane benzeri kokuya sahiptir ve bazı türleri çay veya baharat olarak kullanılabilir. Ayrıca bahçelerde renkli ve çekici görünümleriyle dikkat çeken bitkilerden biridir."
)
BirdOfParadise=Flower(
    name="Bird Of Paradise (Starliçe)",
    habitat="Starliçe, Güney Afrika'da doğal olarak yetişir. Genellikle sıcak iklimleri tercih eder ve sıcak bölgelerde yetiştirilir.",
    color="Çiçeklerin renkleri parlak turuncu ve mavi tonlarında olabilir. Çiçek tüyleri ve taç yaprakları zengin renkli ve ilgi çekici bir görünüme sahiptir.",
    characteristics="Starliçe Çiçeği, büyük, parlak ve benzersiz çiçekleri ile tanınır. Çiçeklerin şekli, gerçekten bir kuşun kanatlarına benzediği düşünüldüğü için bu adı almıştır. Bitkinin yaprakları da geniş ve mızrak şeklindedir. Ayrıca bitki, yüksekliği nedeniyle iç mekanlarda dekoratif bir bitki olarak da yetiştirilebilir."
)
BishopOfLlandaff=Flower(
    name="Bishop Of Llandaff (Llandaff Piskoposu)",
    habitat="Bu çiçeğin doğal olarak yetiştiği yer hakkında net bir bilgi bulunmamaktadır, ancak çoğunlukla bahçelerde yetiştirilen bir çiçek türüdür.",
    color=" Genellikle parlak kırmızı renkte çiçeklere sahiptir.",
    characteristics="'Bishop Of Llandaff' çiçeği, çok gösterişli ve çarpıcı bir görünüme sahip olan bir çeşit daylily türüdür. Yaprakları uzun ve ince yapılıdır. Çiçekleri oldukça büyük ve kırmızı renkte olup, tam güneş ışığı altında en iyi renklerini sergiler. Bahar ve yaz aylarında çiçek açar ve bahçelerde süs bitkisi olarak sıkça tercih edilir. Daylily türleri genellikle dayanıklı ve bakımı kolay bitkiler olarak bilinirler. 'Bishop Of Llandaff' da bu türün güzel bir temsilcisidir."
)
BlackberryLily=Flower(
    name="Blackberry Lily (Böğürtlen Zambağı)",
    habitat="Kuzey Amerika, Avrupa ve Asya'nın bazı bölgelerinde doğal olarak bulunur.",
    color=" Çeşitlilik gösteren renklere sahip olabilir, genellikle turuncu tonları yaygındır.",
    characteristics="Böğürtlen zambağı, dayanıklı bir bitki türüdür. Yaprakları uzun ve şerit şeklindedir. Yaz aylarında gösterişli çiçekler açar. Çiçekler, böğürtlen meyvesini andıran siyah beneklere sahip olması nedeniyle 'Böğürtlen Zambağı' olarak adlandırılır. Bu bitki, bahçe düzenlemelerinde ve doğal peyzajlarda dekoratif bir unsur olarak kullanılabilir. Tohumları siyah böğürtlen meyvelerine benzer ve bitkinin adını taşıyan bu benzerlikten gelir."
)
BlackEyedSusan=Flower(
    name="Black-Eyed Susan (Kara Gözlü Susan)",
    habitat="Kuzey Amerika",
    color="Genellikle sarı renkli çiçekleri vardır.",
    characteristics="Kara Gözlü Susan, papatyagiller (Asteraceae) familyasından gelen ve çoğunlukla sarı renkli çiçekleri olan bir çiçek türüdür. Bu bitki genellikle çimenli bölgelerde, kırlarda ve yolların kenarlarında bulunur. İyi bir güneş ışığına ihtiyaç duyar ve bahar ile sonbahar arasında çiçek açar. Çiçekleri, koyu kahverengi ortasındaki siyah benekler nedeniyle 'Kara Gözlü' adını alır. Bu çiçek türü bahçelerde süs bitkisi olarak da yetiştirilir ve renkli çiçekleri ile bahar ve yaz aylarında bahçelere renk katar."
)
BlanketFlower=Flower(
    name="Blanket Flower (Çarşaf Çiçeği)",
    habitat="Kuzey Amerika'nın çeşitli bölgelerinde doğal olarak yetişir. Aynı zamanda bahçelerde yetiştirilir.",
    color="Genellikle parlak renkli çiçekleri vardır; turuncu, kırmızı, sarı gibi renklerde olabilir.",
    characteristics="Çarşaf Çiçeği, papatyagiller (Asteraceae) familyasına aittir. Yıllık veya çok yıllık otlardan oluşur. Çiçekleri güneşli ve sıcak bölgelerde genellikle yazın açar. Çiçekleri renkli yaprakları ve çekici görüntüsüyle dikkat çeker. Peyzaj tasarımında sıklıkla kullanılan çiçeklerden biridir. Aynı zamanda kelebekleri ve diğer böcekleri çektiği için bahçe çeşitliliğini destekler."
)
BoleroDeepBlue=Flower(
    name="Bolero Deep Blue",
    habitat="Bolero Deep Blue çiçeği genellikle Bahçe Anemone veya Anemone de Caen olarak bilinen türlerin bir üyesidir ve Avrupa kökenlidir.",
    color="Çiçekler genellikle zengin mavi veya menekşe mavisi renkte olabilir.",
    characteristics="Bolero Deep Blue çiçekleri, güzel renkleri ve çekici yapısıyla dikkat çeken bir çiçek türüdür. Anemonlara özgü güzellikleri taşıyan bu çiçekler, bahar ve yaz aylarında bahçeleri süslemek için kullanılır. Bolero Deep Blue anemonları, çiçek soğanlarından yetişir ve genellikle çiçek yataklarında, sınırlarda veya saksılarda yetiştirilirler. Bahar aylarında çiçek açarlar ve bahçenize canlı renkler katarlar."
)
Bougainvillea=Flower(
    name="Bougainvillea (Begonvil)",
    habitat="Bougainvillea, sıcak iklimleri tercih eden bir bitki türüdür ve özellikle Güney Amerika, Orta Amerika, Karayipler ve Güneydoğu Asya bölgelerinde yaygın olarak bulunur.",
    color="Bougainvillea'nın çiçekleri genellikle parlak renklidir, en yaygın renkler arasında pembe, mor, kırmızı ve beyaz bulunur.",
    characteristics="Bougainvillea, çoğunlukla tırmanıcı veya yayıcı bir şekle sahip olan ve çitler, pergolalar, duvarlar ve saksılarda yetiştirilebilen bir bitki türüdür. Çiçeklerinin renkleri oldukça çarpıcıdır ve yapraklarının rengi değişkenlik gösterebilir. Bougainvillea, sıcak iklimleri seven bir bitki olduğu için, soğuk hava koşullarına karşı hassas olabilir. Genellikle güneşli ve iyi drene edilmiş topraklarda yetiştirilmesi önerilir."
)
Bromelia=Flower(
    name="Bromelia",
    habitat="Bromelia türleri farklı renklerde çiçeklere sahip olabilir. Genellikle parlak kırmızı, turuncu, pembe veya mor renk tonlarına sahip çiçekleri vardır.",
    color="Kırmızı, beyaz, pembe, sarı...",
    characteristics="Bromelia, tropik ve yarı tropik iklimlerde yetişen dayanıklı bitkilerden biridir. Çoğunlukla epifitik (diğer bitkilerin üzerinde yaşayan) veya tank epifitleri olarak adlandırılan bitkiler grubuna aittir. Yaprakları genellikle sert, sivri uçlu ve bazen dikenli olabilir. Çiçekleri gösterişlidir ve çoğu türde parlak renklerle dikkat çeker. Bazı türlerde çiçeklerin ortasında su birikintisi oluşur, bu suya bazı böcekler ve hayvanlar düşer ve bitkinin besin kaynağı olarak kullanılır. Bromelia türleri ev içi bitki olarak da popülerdir ve ilginç görünümleri ile dekoratif birer obje olarak kullanılabilirler."
)
Buttercup=Flower(
    name="Buttercup (Çobançiçeği)",
    habitat="Buttercup çiçekleri genellikle Avrupa ve Kuzey Amerika gibi ılıman bölgelerde yetişir.",
    color="Buttercup çiçekleri genellikle parlak sarı renge sahiptir, ancak bazı türleri beyaz veya pembe renkte olabilir.",
    characteristics="Buttercup çiçekleri 5 taç yapraklıdır ve tipik olarak yuvarlak veya yürek şeklinde yaprakları vardır. Çiçekler genellikle çimenlik alanlarda, otlaklarda ve sulak bölgelerde görülür. Tıpkı diğer bazı türler gibi, Buttercup da zehirli özelliklere sahip olabilir. Bu nedenle doğada rastladığınız Buttercup çiçeklerini yemekten veya cilde temas ettirmekten kaçınmanız önerilir."
)
CalifornianPoppy=Flower(
    name="Californian Poppy (Acem Lalesi)",
    habitat="'Californian Poppy' adından da anlaşılacağı gibi, Kaliforniya eyaletine özgüdür. Ayrıca bazı bölgelerde doğal olarak yetişen bir türdür.",
    color="'Californian Poppy' bitkisinin çiçekleri genellikle parlak turuncu veya sarı renktedir. Bu canlı ve göz alıcı renkleri ile dikkat çeker.",
    characteristics=" 'Californian Poppy' kısa ömürlü bir bitki türüdür ve genellikle yıllık olarak yetiştirilir. Çiçekleri yelpaze şeklinde açılır ve güneşli günlerde açar, akşamları veya bulutlu havalarda kapanabilir. Hafif rüzgarlar veya dokunuşlar, çiçeklerin kapanmasına neden olabilir. Bitkinin yaprakları gri yeşil renkte ve tüylü bir dokuya sahiptir. 'Californian Poppy' bitkisi, doğal bahçelerde veya süs bitkisi olarak yetiştirilebilir."
)
Camellia=Flower(
    name="Camellia (Kamelya)",
    habitat="Kamelyalar özellikle Uzak Doğu kökenlidir. Japonya ve Çin gibi bölgelerde doğal olarak yetişirler. Ayrıca çeşitli iklim koşullarına uygun olarak pek çok farklı türü yetiştirilebilir.",
    color="Kamelyalar genellikle beyaz, pembe, kırmızı ve bazen sarı renkte çiçeklere sahiptir.",
    characteristics="Kamelyalar, genellikle yeşil yaprakları ve büyük, gösterişli çiçekleri ile tanınır. Çiçekler genellikle tek veya çift katmanlı yapılardır ve zengin renkleri ile dikkat çekerler. Kamelyalar çeşitli türleri ve çiçek şekilleri ile bilinir. Genellikle kış aylarında çiçek açarlar ve soğuğa dayanıklıdırlar."
)
CannaLily=Flower(
    name="Canna Lily (Kana çiçeği)",
    habitat="Canna Lily çiçeği tropikal ve subtropikal bölgelerde yaygın olarak yetişir. Özellikle Orta ve Güney Amerika, Afrika ve Asya'nın bazı bölgelerinde bulunabilir.",
    color="Canna Lily'nin çiçekleri genellikle parlak ve canlı renklere sahiptir. Kırmızı, turuncu, sarı, pembe ve beyaz gibi farklı renk varyasyonları bulunabilir.",
    characteristics="Canna Lily bitkisi büyük ve gösterişli yapraklara sahip, yüksek büyüyebilen bir bitkidir. Çiçekleri çeşitli renklerde olabilir ve genellikle salkım şeklinde düzenlenmişlerdir. Canna Lily bitkisi genellikle su kenarları, bataklıklar veya nemli topraklarda yetişir. Gösterişli çiçekleri ve yaprakları nedeniyle peyzaj düzenlemelerinde yaygın olarak kullanılır. Ayrıca, bitkinin yumruları yenilebilir ve bazı türleri tıbbi amaçlar için kullanılabilir."
)
CanterburyBells=Flower(
    name="Canterbury Bells",
    habitat="Avrupa'nın çeşitli bölgeleri, özellikle İngiltere",
    color="Çeşitli renklerde bulunabilir, genellikle mavi, mor, pembe ve beyaz tonları görülür.",
    characteristics="Canterbury Zilleri, zengin ve gösterişli çiçek salkımlarıyla tanınan bir çiçektir. Üst üste sıralanmış çan şeklindeki çiçekleri nedeniyle 'Canterbury Zilleri' adını alır. Genellikle ilkbahar ve yaz aylarında çiçek açarlar. Bahçe peyzajlarında süs bitkisi olarak sıkça kullanılırlar ve çiçek yataklarında, sınırlarda veya saksılarda yetiştirilebilirler. Canterbury Zilleri, doğru bakım ve uygun koşullar altında uzun yıllar boyunca güzel çiçeklerini sergileyebilir."
)
CapeFlower=Flower(
    name="Cape Flower",
    habitat="Güney Afrika'nın çeşitli bölgelerinde yetişir.",
    color="Farklı türleri ve çeşitleri olduğu için çeşitli renklerde çiçekleri bulunabilir. Genellikle beyaz, pembe, mor veya kırmızı tonlarında olabilir.",
    characteristics="Cape Çiçeği, 'Gerbera' olarak da bilinir, genellikle büyük ve renkli çiçekleriyle tanınır. Çiçekleri genellikle güneşe dayanıklıdır ve bahar ve yaz aylarında bolca çiçek açarlar. Yaprakları genellikle parlak yeşil ve halkalı şekildedir. Bahçelerde süs bitkisi olarak yetiştirilen popüler bir çiçek türüdür. Schnittblumen (kesme çiçekleri) olarak da kullanılır."
)
Carnation=Flower(
    name="Carnation (Karanfil)",
    habitat=" Orta ve Güney Avrupa, Doğu Asya ve Kuzey Afrika bölgelerinde doğal olarak yetişir. Ancak birçok farklı türü ve çeşidi dünya genelinde yetiştirilmektedir",
    color="Karanfil çiçekleri beyaz, pembe, kırmızı, sarı ve mor gibi farklı renklerde olabilir.",
    characteristics="Karanfil çiçeği, tatlı ve hoş kokusuyla tanınır. Çiçekleri çeşitli renklerde olabilir ve tüylü yaprakları vardır. Klasik bir kesme çiçeği olarak sıkça kullanılır ve bu nedenle çiçek aranjmanları, buketler ve çeşitli dekoratif amaçlar için tercih edilir. Karanfil çiçekleri aynı zamanda bahçe bitkisi olarak da yetiştirilir ve peyzaj düzenlemelerinde kullanılır. Karanfil türleri arasında bazıları daha büyük ve daha gösterişli çiçeklere sahipken, diğerleri daha küçük ve zarif çiçeklere sahip olabilir."
)
CautleyaSpicata=Flower(
    name="Cautleya Spicata",
    habitat="Cautleya Spicata, Himalayalar'ın yüksek bölgelerinde yetişir.",
    color="Cautleya Spicata çiçekleri genellikle kırmızı veya turuncu renktedir.",
    characteristics="Cautleya Spicata, zencefil familyasına ait bir bitki türüdür. Yaklaşık 1 metreye kadar uzayabilen yaprakları ve göz alıcı renkteki çiçekleriyle bilinir. Çiçekleri zencefil benzeri bir görünüme sahiptir ve bitkinin çekici bir görünümü vardır. Cautleya Spicata, soğuk iklimlerde yetiştirilebilir ve bahçelerde dekoratif bir bitki olarak tercih edilebilir. Ayrıca, bahar ve yaz aylarında çiçek açar ve çevresine hoş bir renk ve canlılık katar."
)
Clematis=Flower(
    name="Clematis",
    habitat="Genellikle Avrupa, Kuzey Amerika ve Asya bölgelerinde doğal olarak bulunur.",
    color="Clematis çiçekleri genellikle mor, mavi, beyaz, pembe, kırmızı ve sarı tonlarında olabilir.",
    characteristics=" Clematis, genellikle tırmanıcı bir bitki olarak bilinir. Çiçekleri çeşitli renklerde olabilir ve farklı türleri farklı büyüklüklerde çiçeklere sahip olabilir. Clematis türleri, bahar ve yaz aylarında çiçek açabilir. Görsel olarak çekici ve zarif çiçekleri nedeniyle bahçelerde, çitlerde ve pergolalarda yaygın olarak yetiştirilir. İyi drene edilmiş toprakları ve güneşli yerleri tercih eder. Clematis türleri arasında farklı büyüklüklerde çiçekler, yaprak tipleri ve büyüme alışkanlıkları bulunabilir. Bazı türlerin kokulu çiçekleri de bulunabilir."
)
ColtsFoot=Flower(
    name="Colt's Foot (Öksürük otu)",
    habitat="Avrupa ve Asya'nın birçok bölgesinde doğal olarak bulunur.",
    color="Sarı renklidir.",
    characteristics="Öksürük otu bitkisi, sarı renkli çiçekleri ile tanınır. Genellikle ilkbahar ve erken yaz aylarında çiçek açar. Çiçekleri göz alıcıdır ve bu bitkinin yapraklarına benzerlik taşıyan bir yapısı vardır. Öksürük otu bitkisi, bazı geleneksel kullanımlarıyla da bilinir. Tıbbi ve gıda amaçlı kullanım alanları bulunabilir."
)
Columbine=Flower(
    name="Columbine (Çuha çiçeği)",
    habitat="Kuzey Amerika, Avrupa ve Asya'nın bazı bölgeleri",
    color="Farklı renk varyasyonlarına sahip olabilir; mor, mavi, pembe, beyaz, sarı ve kırmızı tonları görülebilir.",
    characteristics="Çuha çiçeği, çiçeklerin zarif ve farklı bir yapısı olan çiçeklerden biridir. Çiçeklerdeki uzun, tüysü benzeri dikenler ve uzun yapraklara sahiptir. Çuha çiçeği genellikle uzun sapları üzerinde büyür ve nispeten hafif gölgeli alanlarda yetişir. Farklı renkleri ve ilginç yapısıyla bahçelerde ve doğal alanlarda sıklıkla tercih edilen bir çiçektir."
)
CommonDandelion=Flower(
    name="Common Dandelion (Karahindiba)",
    habitat="Kuzey Amerika, Avrupa, Asya ve diğer birçok bölgede yaygın olarak bulunan yabani bitki türüdür.",
    color="Sarı",
    characteristics="Yabani Karahindiba, tırtıl şeklindeki yaprakları ve parlak sarı çiçekleri ile tanınır. Genellikle çayırlarda, parklarda ve bahçelerde rastlanır. Rüzgarla savrulan tohumları vardır ve bu tohumlar rüzgarın etkisiyle yayılırlar. Yaprakları genellikle dişlidir ve genç yaprakları salata olarak tüketilebilir. Aynı zamanda geleneksel tıp alanında kullanılan bir bitkidir."
)
CornPoppy=Flower(
    name="Corn Poppy (Gelincik)",
    habitat="Kırmızı gelincik genellikle tarlalarda, yol kenarlarında ve açık arazilerde yetişir. Tarım alanlarına renk katar ve sıklıkla tahıl tarlalarında görülebilir.",
    color="Çoğunlukla parlak kırmızı renge sahip olan kırmızı gelincikler, bazen pembe, beyaz veya mor tonlarında da bulunabilir.",
    characteristics="Kırmızı gelincik, gelincikgiller (Papaveraceae) familyasına ait bir çiçek türüdür. Tek yıllık veya iki yıllık bitki olarak yetişebilir. Gösterişli kırmızı çiçekleri ve ince saplarıyla tanınır. Tarlalarda ve boş arazilerde sıkça rastlanır. Kırmızı gelincikler genellikle ilkbahar ve yaz aylarında çiçeklenir ve tarım alanlarına renk ve güzellik katarlar."
)
flowers_list.append(ColtsFoot)
flowers_list.append(CautleyaSpicata)
flowers_list.append(AlpineSeaHolly)
flowers_list.append(Anthurium)
flowers_list.append(Artichoke)
flowers_list.append(Azalea)
flowers_list.append(BallMoss)
flowers_list.append(BalloonFlower)
flowers_list.append(BarbetonDaisy)
flowers_list.append(BeardedIris)
flowers_list.append(BeeBalm)
flowers_list.append(BirdOfParadise)
flowers_list.append(BishopOfLlandaff)
flowers_list.append(BlackEyedSusan)
flowers_list.append(BlackberryLily)
flowers_list.append(BlanketFlower)
flowers_list.append(BoleroDeepBlue)
flowers_list.append(Bougainvillea)
flowers_list.append(Bromelia)
flowers_list.append(Buttercup)
flowers_list.append(CalifornianPoppy)
flowers_list.append(Camellia)
flowers_list.append(CannaLily)
flowers_list.append(CanterburyBells)
flowers_list.append(CapeFlower)
flowers_list.append(Carnation)
flowers_list.append(CautleyaSpicata)
flowers_list.append(Clematis)
flowers_list.append(ColtsFoot)
flowers_list.append(Columbine)
flowers_list.append(CommonDandelion)
flowers_list.append(CornPoppy)

def home(request):
    return JsonResponse({'message': 'Welcome to the Example App!'})

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        image_data = request.FILES.get('image_file')
        if not image_data:
            return JsonResponse({'error': 'No image provided'})     
        # Resmi geçici bir dosyaya kaydet
        print("RESİM: ", image_data)
        temp_image_path = os.path.join(settings.BASE_DIR, 'temp_image.jpg')
        with open(temp_image_path, 'wb') as temp_image:
            for chunk in image_data.chunks():
                temp_image.write(chunk)

        hedef_egitim_dizini = 'C:/Users/mamic/Documents/\BitkiTanima/train' 
        hedef_test_dizini = 'C:/Users/mamic/Documents/\BitkiTanima/test'
        model = load_model('vgg_flower30_dogrucevapveriyoryuzde80_model.h5')
        kategoriler = os.listdir(hedef_egitim_dizini)
        
        # Resmi aç ve işle
        img = Image.open(temp_image_path).resize((224, 224))
        img = np.array(img)
        img = img.reshape(-1, 224, 224, 3)
        img = preprocess_input(img)
        preds = model.predict(img)
        en_yuksek_tahmin_indeksi = np.argmax(preds)
        en_yuksek_tahmin_sinifi = kategoriler[en_yuksek_tahmin_indeksi]
        en_yuksek_tahmin_yuzdesi = np.max(preds)
        top_predicted_flower = None
        for cicek in flowers_list:
            if en_yuksek_tahmin_sinifi in cicek.name:
                print("Adı: ", cicek.name)
                print("Yetiştiği Yerler: ", cicek.habitat)
                print("Rengi: ", cicek.color)
                print("Genel Bilgiler: ", cicek.characteristics)
                print(f"Tahmin Yüzdesi: {en_yuksek_tahmin_yuzdesi:.2%}")
                top_predicted_flower = cicek
                break
        
        if top_predicted_flower is not None:
            response_data = {
                "Ad": top_predicted_flower.name,
                "Habitat": top_predicted_flower.habitat,
                "Renk": top_predicted_flower.color,
                "Genel Ozellikler": top_predicted_flower.characteristics
            }
        else:
            response_data = {"Ad": "Bilinmeyen", "Hata": "Tahmin sonucu çiçek listesinde bulunamadı."}

        formatted_predictions = [
            {
                "Ad": top_predicted_flower.name,
                "Renk": top_predicted_flower.color,
                "Habitat": top_predicted_flower.habitat,
                "Genel": top_predicted_flower.characteristics,
                "Yuzde": f"{en_yuksek_tahmin_yuzdesi * 100:.2f}%"
            }
        ]
       
        response_data = {'predictions': formatted_predictions}
        os.remove(temp_image_path)
        
        return JsonResponse(response_data)   

"""img = Image.open("clematis.jpg").resize((224,224))
img = np.array(img)
img.shape
print(img.ndim)
img = img.reshape(-1,224,224,3)
print(img.shape)
print(img.ndim)
img = preprocess_input(img)
preds = model.predict(img)
preds
en_yuksek_tahmin_indeksi = np.argmax(preds)
en_yuksek_tahmin_sinifi = kategoriler[en_yuksek_tahmin_indeksi]
en_yuksek_tahmin_yuzdesi = np.max(preds) * 100

top_predicted_flower = None
for cicek in flowers_list:
    if en_yuksek_tahmin_sinifi in cicek.name:
        print("Adı: ",cicek.name)
        print("Yetiştiği Yerler: ",cicek.habitat)
        print("Rengi: ",cicek.color)
        print("Genel Bilgiler: ",cicek.characteristics)
        print( "Tahmin Yüzdesi:" f"{en_yuksek_tahmin_yuzdesi:.2f}%")
        top_predicted_flower = cicek
        break

if top_predicted_flower is not None:
    response_data = {
        "Ad": top_predicted_flower.name,
        "Habitat": top_predicted_flower.habitat,
        "Renk": top_predicted_flower.color,
        "Genel Ozellikler": top_predicted_flower.characteristics
    }
else:
    response_data = {"Ad": "Bilinmeyen", "Hata": "Tahmin sonucu çiçek listesinde bulunamadı."}
"""


