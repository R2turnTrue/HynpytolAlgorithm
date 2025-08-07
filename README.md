# Solving HYNPYTOL puzzle game using A-star Algorithm

[흰피톨](https://store.steampowered.com/app/2520000/HYNPYTOL/)은 소코반류 퍼즐 게임입니다. 주인공 'T세포'는 자신의 팔을 끌고 당기며 장애물을 헤쳐나가 목적지에 도달해야 합니다.

흰피톨 챕터 1에서 T세포는 팔을 활용해 이동식 타일인 '단핵구'를 이동할 수 있고, 감염 세포를 맞은 편에서 '하이파이브'해서 제거할 수 있습니다. 모든 감염 세포를 제거한 뒤에 T세포가 목적 지점에 도달하면 승리합니다.

목적지까지의 맨해튼 거리를 휴리스틱으로 A\* 알고리즘을 활용해 흰피톨의 퍼즐을 풀이하는 프로그램을 구현했습니다.

> [!NOTE]
> 현재 이 프로젝트는 흰피톨 챕터 1의 요소 (이동 장애물 단핵구, 감염 세포)만을 구현했습니다. 지금으로선 다른 챕터의 요소는 구현할 계획이 없습니다.

> [!TIP]
> 흰피톨매우재밌으니꼭해보세요

## Demonstration

[![Demonstration](http://img.youtube.com/vi/GRuGJUeIGx0/0.jpg)](https://www.youtube.com/watch?v=GRuGJUeIGx0)

## Prerequisties

-   pygame (길찾기 시각화 / 유저 플레이)
-   pyautogui (자동입력)

## Premade levels

-   해당 레벨들은 원본 게임에서 그대로 가져왔습니다.
    -   `map01.py`: 흰피톨 챕터 1 - 움직이기 전에 생각했나요?
    -   `map02.py`: 흰피톨 챕터 1 - 구르는 돌처럼
    -   `map03.py`: 흰피톨 챕터 1 - 여기여기 붙어라

## Running

### Run pygame frontend (user play)

```
python pygamefe.py <mapfile.py>
```

### Run pathfinder

```
python main.py <mapfile.py>
```

> [!NOTE]
> `main.py`의 상당 플래그를 수정해서 길찾기 과정 시각화를 켜거나 끌 수 있습니다.

### Run pathfinder + macro

```
python macro.py <mapfile.py>
```
