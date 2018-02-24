
# System-Monitor-V2

An updated version of `system-monitor`. Uses socket.io instead jquery polling. The idea is to follow a way of working with mini-sprints, 45 minutes of focused work with a releasable version after each iteration. 

### Technologies used
| Name    | Description     |
|-------------|-------------|
|             |             |
|`flask`||
|`socket.io`        | propagate state from backend to browser |
|`fullPage.js`      | generates "powerpoint" like pages   |
|**Plugins**||
|`showdown.js`      | markdown to html   |
| **Development**    ||
| `live.js`      | reload page on change |

### Sprint log
| Sprint #    | Target      | Completed   | Time (actual)  |
|-------------|-------------|-------------|-------------|
|             |             |             |             |
|             |             |             |             |
|             |             |             |             |
|             |  Configurable .md file  |             |             |
|  5  | Use `Showdown.js` to turn markdown to html|             |    45 min <br>(45)    |
|  4  |  Break markdown into sections<br>Release 0.3 | ~~Break markdown into sections~~<br>~~Release 0.3~~ |    45 min (43)         |
|  3  | Introduce live.js<br>Break markdown into sections<br>Add content from file<br>Generate config.yaml<br>Release 0.3 | ~~Introduce live.js~~<br>Break markdown into sections<br>~~Add content from config.yaml~~<br>Generate config.yaml<br>Release 0.3 |   45 min<br>(45)  |
|  ~  | ~ | Skunk worked on `Showdown`|     (55 min)     |
|  2  | Add socket.io prerequisites<br>Broadcast slide/index to other users<br>Master mode for clients<br>Follow broadcast<br>Release 0.2 | ~~Add socket.io prerequisites~~<br>~~Broadcast slide/index to other clients~~<br>~~Client follow master position~~<br>~~Release 0.2~~ |  45 min<br>(43) |
|  1  | Initialize repo<br>Create README.md<br>Copy files from `system-monitor`<br>Simple 3 page system up<br>Release 0.1<br>Finish on time | ~~Initialize repo~~<br>~~Create README.md~~<br>~~Copy files from `system-monitor`~~<br>~~Simple 3 page system up~~<br>~~Release 0.1~~<br>~~Finish on time~~ |  45 min  |
|             |             |             |             |
|             |             |             |   **2h23 min**    |

## TODOs
* Handle pages without title as first line

## Ideas
* List # users
* Ask to take control from master
* Dockerfile
* Animated gif for documentation
* Include [highlight.js](https://highlightjs.org/)
* (probably a separate repo). Create sections of HTML from markdown
* Show an overlay of the available pages in upper right corner
* Document formats: Complete HTML
* List of available document
* Use [showdown prettify](https://github.com/showdownjs/prettify-extension)



## Releases

#### 0.4
* Document formats: Markdown file

#### ~~0.3~~
* ~~Introduce live.js~~
* ~~Lib to break down markdown files to html~~

#### ~~0.2~~
* Add socket.io prerequisites
* Broadcast slide/index to other users
* Master mode for clients
* Follow broadcast

#### ~~0.1~~
* Initialize repo
* Create README.md
* Copy files from `system-monitor`
* Simple 3 page system up
