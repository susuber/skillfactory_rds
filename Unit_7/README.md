![Title PNG "Skill Factory"](skillfactory_logo.png)
# Проект №7. Выбираем авто выгодно

<!-- vim-markdown-toc Redcarpet -->

* [Состав команды](#состав-команды)
* [Задача](#задача)
* [Описание датасета](#описание-датасета)
* [Структура репозитория](#структура-репозитория)
* [Выводы](#выводы)

<!-- vim-markdown-toc -->

## Состав команды: 
[Сергей](https://github.com/KuzovovSS), [Евгения](https://github.com/Zhulik2018), [Александр](https://github.com/susuber).

Название команды на kaggle.com: DSPR-54.

[Отчетный ноутбук](Choose_a_car_profitably2.ipynb) и [Ноутбук](APP6.ipynb)

## Задача

https://www.kaggle.com/c/sf-dst-car-price-prediction/overview

## Описание датасета:
- **bodyType** - тип кузова
- **brand** - бренд авто
- **car_url** - ссылка объявление на сайте
- **color** - цвет авто
- **complectation_dict** - cловарь оборудования, входящего в комплектацию
- **description** - реклама салона, условия продавца
- **engineDisplacement** - объём двигателя, л.
- **enginePower** - мощность двигателя, л.с.
- **equipment_dict** - cловарь оборудования, входящего в комплектацию, частично дублирует complectation_dict
- **fuelType** - тип потребляемого топлива
- **image** - ссылка на фото авто на сайте
- **mileage** - пробег, км
- **modelDate** - дата начала выпуска данной модели
- **model_info** - cловарь с данными о модели
- **model_name** - название модели
- **name** - данные об объёме двигателя, мощности авто и типе коробки передач
- **numberOfDoors** - количество дверей
- **parsing_unixtime** - время парсинга
- **priceCurrency** - валюта, в которой указана стоимость авто на сайте
- **productionDate** - дата производства
- **sell_id** - ID номер в базе
- **super_gen** - cловарь с техническими характеристиками
- **vehicleConfiguration** - признак дублирующий (bodyType, engineDisplacement и vehicleTransmission)
- **vehicleTransmission** - тип коробки передач
- **vendor** - регион первичной продажи/производства авто
- **Владельцы** - сведения о количестве предыдущих владельцев
- **Владение** - время последнего владения
- **ПТС** - вид паспорта транспортного средства
- **Привод** - тип привода
- **Руль** - положение руля
- **Состояние** - состояние, в котором находится продаваемое авто
- **Таможня** - сведения о таможне

## Структура репозитория:

[parsing_by_car_brands.py](parsing_by_car_brands.py) - скрипт для парсинга данных о продоваемых поддержаных машинах в городе Москва с сайта [auto.ru](https://auto.ru/) по списку брендов до 20.02.2022 г.

[parsing_for_file_links.py](parsing_for_file_links.py) - скрипт для парсинга данных о продоваемых поддержаных машинах в городе Москва с сайта [auto.ru](https://auto.ru/) по списку ссылок на страницы с продоваемыми машинами до 20.02.2022 г.

[New_parsing_by_car_brands.py](New_parsing_by_car_brands.py) - скрипт для парсинга данных о продоваемых поддержаных машинах в городе Москва с сайта [auto.ru](https://auto.ru/) по списку брендов после 20.02.2022 г. (ввиду смены верстки страниц сайта)

[Choose_a_car_profitably2.ipynb](Choose_a_car_profitably2.ipynb) - ноутбук с полным и еда выводами, а также переобучением модели, вызванное большим колличеством данных

[APP6.ipynb](APP6.ipynb) - первый ноут бук с первым беглым EDA не имеющий дополнительных данных полученных при парсинге и результатом зафиксированном на [Kaggle](https://www.kaggle.com/c/sf-dst-car-price-prediction/leaderboard)

## Выводы:

[XGBoost](https://xgboost.readthedocs.io) и [LightGBM](https://lightgbm.readthedocs.io) очень мощные библиотеки для построения моделей градиентного бустинга на решающих деревьях. Преимущества [LightGBM](https://lightgbm.readthedocs.io):быстрая скорость обучения и высокая эффективность.

Алгоритм [XGBoost](https://xgboost.readthedocs.io) обладает высокой предсказательной способностью и в разы быстрее любых других методов градиентного бустинга, включает в себя различные регуляризации, что уменьшает переобучение и улучшает общую производительность. 

[RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) имеет следующие преимущества:
* имеет высокую точность предсказания, которая сравнима с результатами градиентного бустинга; 
* не требует тщательной настройки параметров, хорошо работает из коробки; 
* редко переобучается; 
* на практике добавление деревьев только улучшает композицию; 
* хорошо работает с пропущенными данными – сохраняет хорошую точность даже при их наличии.    

В [Catboost](https://catboost.ai/) прогнозы делаются на основе ансамбля слабых обучающих алгоритмов. В отличие от случайного леса, который создает дерево решений для каждой выборки, в градиентном бустинге деревья создаются последовательно. Предыдущие деревья в модели не изменяются. Результаты предыдущего дерева используются для улучшения последующего.

В мире машинного обучения одними из самых популярных типов моделей являются решающее дерево и ансамбли на их основе. 
Преимуществами деревьев являются: 
* простота интерпретации, 
* нет ограничений на вид исходной зависимости, 
* мягкие требования к размеру выборки. 

Деревья имеют и крупный недостаток — склонность к переобучению. Поэтому почти всегда деревья объединяют в ансамбли: случайный лес, градиентный бустинг и др. Сложными теоретическими и практическим задачами являются составление деревьев и объединение их в ансамбли. [Extra Trees](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html) — это метод ансамблевого обучения, который объединяет результаты нескольких не коррелированных деревьев решений, собранных в «лесу», для вывода результатов.

Лучшим из рассмотренных себя проявил [staking](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingRegressor.html) моделей [Catboost](https://catboost.ai/), [XGBoost](https://xgboost.readthedocs.io), [Extra Trees](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html) и [LightGBM](https://lightgbm.readthedocs.io) с мета моделью линейной регрессии. В процессе работы оказалось справедливом следующее предположение : поскольку в [staking](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingRegressor.html) мета-модель обучается на ответах уже натренированных алгоритмов, то они сильно коррелируют. Для борьбы с этим часто базовые алгоритмы не сильно оптимизируют как и было сделано в нашем случае  
