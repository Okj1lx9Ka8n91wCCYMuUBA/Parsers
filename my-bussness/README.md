
# Парсер Портал “Мой бизнес” ([мойбизнес.рф](мойбизнес.рф))

## Запуск

```bash
pip install -r ./../requirements.txt
```

Параметр `USE_KAFKA` позволяет запустить файл `main.py` как скрипт без использования `kafka`.

```bash
python ./my-bussness/main.py
```

## Пример вывода

```json
Результат: [
    {
        "title": "Всероссийский рейтинг малого и среднего бизнеса «Индекс дела»",
        "url": "https://мойбизнес.рф/anticrisis/vserossiyskiy-reyting-malogo-i-srednego-biznesa-indeks-dela",
        "description": "Новый системный инструмент развития для предпринимателей"
    },
    {
        "title": "Поддержка от АНО «Мой бизнес – мои возможности», Минэкономразвития и Яндекс Директ",
        "url": "https://мойбизнес.рф/anticrisis/podderzhka-ot-ano-moy-biznes-moi-vozmozhnosti-minekonomrazvitiya-i-yandeks-direkt",
        "description": "Предприниматели могут получить 7 000₽ на первую рекламную кампанию в Яндекс Директе"
    },
    {
        "title": "Поддержка малого и среднего бизнеса от Минэкономразвития и Яндекс Бизнеса",
        "url": "https://мойбизнес.рф/anticrisis/podderzhka-malogo-i-srednego-biznesa-ot-minekonomrazvitiya-i-yandeks-biznesa",
        "description": "До 27 декабря 2024 года предприниматели могут получить 7 000₽ на запуск первой рекламы и помощь в запуске рекламной кампании"
    },
    {
        "title": "Программа поддержки от Минэкономразвития России, Росмолодежь и SuperJob",
        "url": "https://мойбизнес.рф/anticrisis/programma-podderzhki-ot-minekonomrazvitiya-rossii-rosmolodezh-i-superjob",
        "description": "Компании по всей России могут бесплатно разместить на SuperJob вакансии на позиции стажеров, чтобы нанять молодых специалистов"
    },
    {
        "title": "Поддержка Минэкономразвития и «Ярмарка Мастеров – Livemaster» для мастеров и ремесленников",
        "url": "https://мойбизнес.рф/anticrisis/podderzhka-minekonomrazvitiya-rossii-i-yarmarka-masterov-livemaster-dlya-predprinimateley-sfery-krea",
        "description": "Минэкономразвития России на базе Центров «Мой бизнес» и маркетплейс Ярмарка Мастеров − Livemaster проводят конкурс для ремесленников и представителей креативных индустрий"
    },
    {
        "title": "Программа поддержки предпринимателей от Минэкономразвития России и Авито",
        "url": "https://мойбизнес.рф/anticrisis/programma-podderzhki-predprinimateley-sfery-uslug-ot-minekonomrazvitiya-rossii-i-avito",
        "description": "Минэкономразвития России и Авито расширили программу по поддержке малых и средних предпринимателей на более выгодных для бизнеса условиях"
    },
    {
        "title": "Программа поддержки соцбизнеса от hh.ru и Минэкономразвития России",
        "url": "https://мойбизнес.рф/anticrisis/programma-podderzhki-sotsbiznesa-ot-hh-ru-i-minekonomrazvitiya-rossii",
        "description": "Нужна помощь в поиске людей на свой проект? Воспользуйтесь услугой бесплатного поиска сотрудников на hh.ru с помощью нашей меры поддержки"
    },
    {
        "title": "Программы льготного кредитования",
        "url": "https://мойбизнес.рф/anticrisis/antikrizisnye-programmy-lgotnogo-kreditovaniya-msp-ot-banka-rossii",
        "description": "Антикризисные программы льготного кредитования бизнеса"
    },
    {
        "title": "Расширение доступа к соцконтрактам",
        "url": "https://мойбизнес.рф/anticrisis/rasshirenie-dostupa-k-sotskontraktam",
        "description": "Рассказываем, как получить до 350 тыс. руб. от государства на открытие своего дела."
    },
    {
        "title": "Поручительства и гарантии в случае отсутствия залога",
        "url": "https://мойбизнес.рф/anticrisis/poruchitelstva-i-garantii-v-sluchae-otsutstviya-zaloga",
        "description": "Предприниматели могут получить поручительство, если им не хватает залогового обеспечения, чтобы получить банковский кредит, гарантию, лизинг"
    },
    {
        "title": "Гранты для молодых предпринимателей",
        "url": "https://мойбизнес.рф/anticrisis/granty-dlya-molodykh-predprinimateley",
        "description": "Граждане до 25 лет, которые решили открыть свое дело, смогут получить грант  от государства до 1 млн рублей."
    },
    {
        "title": "Экспресс-займы для малого и среднего бизнеса",
        "url": "https://мойбизнес.рф/anticrisis/ekspress-zaymy-dlya-malogo-i-srednego-biznesa",
        "description": "Экспресс-поддержка бизнеса от МСП Банка"
    },
    {
        "title": "Федеральная программа «Мама-предприниматель»",
        "url": "https://мойбизнес.рф/anticrisis/federalnaya-programma-mama-predprinimatel",
        "description": "Участницы проекта получат комплексные знания для открытия своего дела, а для лучших бизнес-идей в каждом регионе предусмотрен грант в 100 тысяч рублей на реализацию"
    },
    {
        "title": "Мораторий на проверки предприятий и предпринимателей",
        "url": "https://мойбизнес.рф/anticrisis/moratoriy-na-proverki-predpriyatiy-i-predprinimateley",
        "description": "В России до конца 2024 года будет действовать мораторий на проведение проверок бизнеса."
    },
    {
        "title": "На портале госуслуг можно заявить о нарушениях моратория на проверки",
        "url": "https://мойбизнес.рф/anticrisis/na-portale-gosuslug-mozhno-zayavit-o-narusheniyakh-moratoriya-na-proverki",
        "description": "В этом году правительство усилило контроль за соблюдением ограничений на проведение проверок бизнеса."
    },
    {
        "title": "Освобождение ввозимого оборудования от НДС",
        "url": "https://мойбизнес.рф/anticrisis/osvobozhdenie-vvozimogo-oborudovaniya-ot-nds",
        "description": "В перечень оборудования, ввоз которого освобождается от налога на добавленную стоимость (НДС), внесены новые позиции."
    },
    {
        "title": "Льготы на ввоз продуктов и сырья",
        "url": "https://мойбизнес.рф/anticrisis/lgoty-na-vvoz-produktov-i-syrya",
        "description": "Совет ЕАК принял решение на 6 месяцев освободить от ввозной таможенной пошлины ряд товаров."
    },
    {
        "title": "Отсрочка внедрения поэкземплярного учета молочной продукции",
        "url": "https://мойбизнес.рф/anticrisis/otsrochka-vnedreniya-poekzemplyarnogo-ucheta-molochnoy-produktsii",
        "description": "Поэкземплярное отслеживание молочной продукции перенесено более чем на 1,5 года – до 1 июня 2025 года."
    },
    {
        "title": "Выкуп земельных участков без торгов",
        "url": "https://мойбизнес.рф/anticrisis/vykup-zemelnykh-uchastkov-bez-torgov",
        "description": "Предприниматели, налаживающие производство импортозамещающей продукции, смогут получить земельные участки в аренду без проведения торгов."
    },
    {
        "title": "Меры поддержки IT-компаний",
        "url": "https://мойбизнес.рф/anticrisis/mery-podderzhki-it-kompaniy",
        "description": "Президент РФ установил комплекс мер для ускоренного развития IT-отрасли."
    },
    {
        "title": "Производственные цепочки и партнеры",
        "url": "https://мойбизнес.рф/anticrisis/proizvodstvennye-tsepochki-i-partnery",
        "description": "Упрощение получения сертификатов соответствия техническим регламентам, запрет на возврат (реэкспорт) оборудования, снижение/обнуление ввозных таможенных пошлин на отдельные товары."
    },
    {
        "title": "Изменение цены госконтракта",
        "url": "https://мойбизнес.рф/anticrisis/izmenenie-tseny-goskontrakta",
        "description": "Механизм поддержки строительной отрасли, который помогает компенсировать дополнительные расходы застройщиков, продлевается до конца 2022 года."
    },
    {
        "title": "Повышенные авансы по госконтрактам",
        "url": "https://мойбизнес.рф/anticrisis/povyshennye-avansy-po-goskontraktam",
        "description": "Компании, участвующие в госзакупках, смогут получать в 2022 году в качестве аванса до 90% от цены контракта."
    },
    {
        "title": "Финансирование инвестпроектов в сфере промышленности",
        "url": "https://мойбизнес.рф/anticrisis/finansirovanie-investproektov-v-sfere-promyshlennosti",
        "description": "На предоставление льготных займов промышленным предприятиям, которые занимаются разработкой продукции, способной заменить зарубежные аналоги, будет дополнительно направлено 20 млрд рублей."
    },
    {
        "title": "Финансирование разработок конструкторской документации для импортозамещения",
        "url": "https://мойбизнес.рф/anticrisis/finansirovanie-razrabotok-konstruktorskoy-dokumentatsii-dlya-importozameshcheniya",
        "description": "Михаил Мишустин подписал постановление, увеличивающее долю государственного финансирования в грантах на создание отечественных комплектующих для различных отраслей промышленности."
    },
    {
        "title": "Льготные кредиты под 3% для инновационных компаний",
        "url": "https://мойбизнес.рф/anticrisis/lgotnye-kredity-pod-3-dlya-innovatsionnykh-kompaniy",
        "description": "Кредит по льготной ставке для высокотехнологичного малого и среднего бизнеса в рамках государственной программы «Взлет — от стартапа до IPO»"
    },
    {
        "title": "0% налог на прибыль для IT-компаний",
        "url": "https://мойбизнес.рф/anticrisis/0-nalog-na-pribyl-dlya-it-kompaniy",
        "description": "IT-компании, которые ранее платили налог на прибыль по ставке 3%, полностью освободят от уплаты налога на прибыль в 2022–2024 годах."
    },
    {
        "title": "Урегулирование задолженности",
        "url": "https://мойбизнес.рф/anticrisis/uregulirovanie-zadolzhennosti",
        "description": "Изменение расчета пеней, реструктуризация задолженности вместо банкротства, приостановление блокировки счетов."
    },
    {
        "title": "Приостановлены выездные налоговые проверки IT-компаний",
        "url": "https://мойбизнес.рф/anticrisis/priostanovleny-vyezdnye-nalogovye-proverki-it-kompaniy",
        "description": "ФНС России приостановила выездные (в том числе повторные) налоговые проверки IT-компаний до 3 марта 2025 года."
    },
    {
        "title": "Продление срока уплаты налога по УСН",
        "url": "https://мойбизнес.рф/anticrisis/prodlenie-sroka-uplaty-naloga-po-usn",
        "description": "Срок уплаты налога по УСН за 2021 год и I квартал 2022 года для ИП и организаций из отдельных отраслей экономики продлевается на 6 месяцев."
    },
    {
        "title": "Повышенное авансирование госконтрактов в 2022 году",
        "url": "https://мойбизнес.рф/anticrisis/povyshennoe-avansirovanie-goskontraktov-v-2022-godu",
        "description": "Компании, участвующие в госзакупках, смогут получать в 2022 году в качестве аванса до 90% от цены контракта."
    },
    {
        "title": "Легализация параллельного импорта",
        "url": "https://мойбизнес.рф/anticrisis/legalizatsiya-parallelnogo-importa",
        "description": "Правительство приняло решение разрешить ввоз в страну востребованных оригинальных товаров иностранного производства без согласия правообладателей."
    },
    {
        "title": "Сбыт и продвижение",
        "url": "https://мойбизнес.рф/anticrisis/sbyt-i-prodvizhenie",
        "description": "Упрощение процедур в части государственных закупок, поддержка МСП и самозанятых при закупках по 223-ФЗ."
    },
    {
        "title": "Аграриям возместят затраты на выращивание овощей и строительство теплиц",
        "url": "https://мойбизнес.рф/anticrisis/agrariyam-vozmestyat-zatraty-na-vyrashchivanie-ovoshchey-i-stroitelstvo-teplits",
        "description": "Правительство расширит поддержку производителей картофеля и других овощей."
    },
    {
        "title": "Меры поддержки для плательщиков налога на прибыль и НДС",
        "url": "https://мойбизнес.рф/anticrisis/mery-podderzhki-dlya-platelshchikov-naloga-na-pribyl-i-nds",
        "description": "Совет Федерации одобрил законопроект, предусматривающий реализацию антикризисных мер поддержки в условиях санкционных ограничений."
    },
    {
        "title": "Программы бесплатного переобучения",
        "url": "https://мойбизнес.рф/anticrisis/programmy-besplatnogo-pereobucheniya",
        "description": "С 28 марта на портале «Работа России» открыта запись на переобучение. Обучение можно пройти бесплатно и получить знания по востребованным в вашем регионе профессиям."
    },
    {
        "title": "Продление срока уплаты авансового платежа по налогу на прибыль до 28 апреля",
        "url": "https://мойбизнес.рф/anticrisis/prodlenie-sroka-uplaty-avansovogo-platezha-po-nalogu-na-pribyl-do-28-aprelya",
        "description": "Речь идёт об авансовом платеже по налогу на прибыль за I квартал 2022 года."
    },
    {
        "title": "Смягчение требований к маркировке молока и воды",
        "url": "https://мойбизнес.рф/anticrisis/smyagchenie-trebovaniy-k-markirovke-moloka-i-vody",
        "description": "Правительство отложило до 1 декабря 2023 года введение обязательной маркировки молочной продукции для фермерских хозяйств и сельскохозяйственных кооперативов."
    },
    {
        "title": "Гранты для туристической отрасли",
        "url": "https://мойбизнес.рф/anticrisis/granty-dlya-turisticheskoy-otrasli",
        "description": "Ростуризм запустил 3 новые грантовые программы в туризме."
    },
    {
        "title": "Обнуление ставки НДС для гостиничного бизнеса",
        "url": "https://мойбизнес.рф/anticrisis/obnulenie-stavki-nds-dlya-gostinichnogo-biznesa",
        "description": "В России будет обнулена ставка НДС для гостиниц и других средств размещения – для работающих и новых отелей."
    },
    {
        "title": "Ускоренный возврат НДС",
        "url": "https://мойбизнес.рф/anticrisis/uskorennyy-vozvrat-nds",
        "description": "Налогоплательщики смогут вернуть НДС в ускоренном порядке уже в апреле."
    },
    {
        "title": "Поддержка для компаний, выпускающих товары из переработанных отходов",
        "url": "https://мойбизнес.рф/anticrisis/podderzhka-dlya-kompaniy-vypuskayushchikh-tovary-iz-pererabotannykh-otkhodov",
        "description": "Предприниматели, выпускающие товары из переработанных отходов, получат господдержку."
    },
    {
        "title": "Отмена проверок бизнеса МВД",
        "url": "https://мойбизнес.рф/anticrisis/otmena-proverok-biznesa-mvd",
        "description": "МВД отменило все плановые проверки бизнеса. Исключение – проверки, которые касаются безопасности."
    },
    {
        "title": "Отмена всех плановых проверок IT-компаний",
        "url": "https://мойбизнес.рф/anticrisis/otmena-vsekh-planovykh-proverok-it-kompaniy",
        "description": "IT-компании на три года освобождаются от плановых проверок."
    },
    {
        "title": "Продление лицензий",
        "url": "https://мойбизнес.рф/anticrisis/prodlenie-litsenziy",
        "description": "Мера затронет более 120 видов разрешений, в том числе в важных сферах деятельности."
    },
    {
        "title": "Ограничение уголовных дел по налоговым преступлениям",
        "url": "https://мойбизнес.рф/anticrisis/ogranichenie-ugolovnykh-del-po-nalogovym-prestupleniyam",
        "description": "Усовершенствован порядок возбуждения уголовных дел о преступлениях, связанных с уклонением от уплаты обязательных платежей."
    },
    {
        "title": "Отмена штрафов по госконтрактам",
        "url": "https://мойбизнес.рф/anticrisis/otmena-shtrafov-po-goskontraktam",
        "description": "Для списания пеней и штрафов подрядчику достаточно представить госзаказчику письменное обоснование."
    },
    {
        "title": "Снижение административной нагрузки на малый бизнес",
        "url": "https://мойбизнес.рф/anticrisis/snizhenie-administrativnoy-nagruzki-na-malyy-biznes",
        "description": "В КоАП внесены изменения для снижения административной нагрузки на малый бизнес."
    },
    {
        "title": "В регионах работают «горячие линии» для поддержки бизнеса",
        "url": "https://мойбизнес.рф/anticrisis/v-regionakh-zapustili-goryachie-linii-dlya-podderzhki-biznesa-vo-vremya-pandemii",
        "description": "Предприниматели могут обращаться за консультациями по мерам антикризисной поддержки по телефонам «горячих линий» в своих регионах."
    }
]
```
