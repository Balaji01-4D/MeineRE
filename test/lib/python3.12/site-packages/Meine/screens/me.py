from pathlib import Path

from textual.containers import Container, Vertical
from textual.events import Click
from textual.screen import ModalScreen
from textual.widgets import Markdown

data = """\
# **About Me**

Hi! I’m **Balaji**, the developer behind this project. I’m a second-year **Computer Science Engineering** student, passionate about building innovative and impactful applications. At 19 years old, I’m always on the lookout for opportunities to grow and create solutions to real-world problems.


### **A Note About This Project**
This is my **first project**, and I’ve put in my best effort to create something functional and helpful. However, as I’m still learning, there might be issues or bugs caused by my inexperience. I appreciate your understanding and would love any feedback to improve this tool further.

Feel free to report any issues, and I’ll do my best to resolve them quickly!

Natural Language Processing (NLP) based cli tool will available soon!


## **Interests**
- **Application Development**: Designing user-friendly and functional software.
- **Problem Solving**: Finding efficient solutions to coding challenges.
- **Learning New Tech**: Constantly exploring new programming languages, tools, and frameworks.

## **Skills**
- **Programming Languages**:
  - Python, Java and C.
- **Technologies Used**:
  - Mobile app development.
  - Basic web design and front-end development.
  - Database systems and management.

## **Goals**
1. Excel in **full-stack development** and enhance my expertise in building robust applications.
2. Collaborate on **open-source projects** to contribute to the developer community.
3. Create solutions that address **real-world challenges** with innovation and efficiency.


### **Libraries and Tools Used**
This project wouldn’t have been possible without the amazing Python libraries that enhanced its functionality and user experience:
- **[Textual](https://github.com/Textualize/textual)**: Used for creating the TUI (Text User Interface) with a clean and interactive layout.
- **[Rich](https://github.com/Textualize/rich)**: For adding beautiful formatting and displaying system information in an eye-catching way.
- **[Pathlib](https://docs.python.org/3/library/pathlib.html)**: For gathering Path-related details.
- **[OS](https://docs.python.org/3/library/os.html)**: For handling file operations such as creating, moving, and deleting files.
- **[Psutil](https://github.com/giampaolo/psutil)**: To fetch detailed system information like CPU, RAM, and disk usage.

A big thanks to the developers and contributors of these libraries!


### **Let’s Collaborate**
If you’d like to collaborate on projects or have any questions, feel free to connect with me:
- **LinkedIn**: [linkedin.com/in/Balaji](https://www.linkedin.com/in/balaji-j-1182b82ba)
- **GitHub**: [github.com/Balaji01-4D](https://github.com/Balaji01-4D)

Together, we can create something amazing!

---
"""


class Myself(ModalScreen):
    CSS_PATH = Path(__file__).parent.parent / "tcss/me.tcss"

    def compose(self):
        yield Container(Vertical(Markdown(markdown=data)))

    def on_click(self, event: Click):
        if str(event.widget) == str(Myself()):
            self.dismiss()
