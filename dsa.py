import sys
import json
import os
import random
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QScrollArea, QCheckBox, QFrame, QGridLayout
)
from PyQt5.QtGui import QColor, QPainter, QFont, QLinearGradient, QBrush
from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QRect, 
    QSize, QTimer, pyqtProperty
)

# Path to the JSON file
JSON_PATH = r"C:\Users\risha\OneDrive\Desktop\Lab Practice\OOPS Lab 2\dsa_progress.json"

# List of motivational quotes
MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The secret of getting ahead is getting started. - Mark Twain",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    "It always seems impossible until it's done. - Nelson Mandela",
    "The best way to predict the future is to create it. - Abraham Lincoln"
]

###############################################################################
#                            CIRCULAR PROGRESS BAR                            #
###############################################################################
class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 150)
        self._progress = 0
        self._targetProgress = 0

        # Animation for smooth progress transitions
        self._animation = QPropertyAnimation(self, b"progress")
        self._animation.setDuration(800)
        self._animation.setEasingCurve(QEasingCurve.OutQuint)

    def getProgress(self):
        return self._progress

    def setProgress(self, value):
        self._progress = value
        self.update()

    progress = pyqtProperty(float, getProgress, setProgress)

    def setTargetProgress(self, value):
        self._targetProgress = value
        self._animation.setStartValue(self._progress)
        self._animation.setEndValue(value)
        self._animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background circle (using a semi-transparent dark shade)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(40, 40, 60, 120))
        painter.drawEllipse(10, 10, self.width() - 20, self.height() - 20)
        
        # Draw progress arc with a modern purple gradient (matches button style)
        if self._progress > 0:
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor("#8e2de2"))
            gradient.setColorAt(1, QColor("#4a00e0"))
            painter.setBrush(QBrush(gradient))
            span_angle = int(-self._progress * 360 * 16)
            painter.drawPie(10, 10, self.width() - 20, self.height() - 20, 90 * 16, span_angle)
        
        # Draw inner circle for hollow effect with a complementary dark color
        painter.setBrush(QColor("#2c3e50"))
        painter.drawEllipse(30, 30, self.width() - 60, self.height() - 60)
        
        # Draw progress percentage text
        painter.setPen(QColor("#ecf0f1"))
        painter.setFont(QFont("Segoe UI", 18, QFont.Bold))
        percentage = int(self._progress * 100)
        painter.drawText(self.rect(), Qt.AlignCenter, f"{percentage}%")

###############################################################################
#                             ANIMATED CHECKBOX                               #
###############################################################################
class AnimatedCheckBox(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.checkbox = QCheckBox(text)

        # Increased font size and light text for better contrast on dark backgrounds
        self.checkbox.setFont(QFont("Segoe UI", 12))
        self.checkbox.setStyleSheet("""
            QCheckBox {
                color: #ecf0f1;  /* Light text for dark background */
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border-radius: 12px;
                border: 2px solid rgba(236, 240, 241, 200);
                background: rgba(236, 240, 241, 40);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #8e2de2, stop:1 #4a00e0);
                border: 2px solid #4a00e0;
            }
            QCheckBox:hover {
                background: rgba(236, 240, 241, 15);
                border-radius: 10px;
            }
        """)

        self.layout.addWidget(self.checkbox)
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Start collapsed; animate expansion for a modern UX feel
        self.setMaximumHeight(0)
        self.animation = QPropertyAnimation(self, b"maximumHeight")
        self.animation.setDuration(600)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.setStartValue(0)
        self.animation.setEndValue(50)
        QTimer.singleShot(100, self.animation.start)

###############################################################################
#                           BUTTON WITH RIPPLE                                #
###############################################################################
class ButtonWithRipple(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self._opacity = 0.7

        # Updated button gradient to a modern vibrant purple scheme
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #8e2de2, stop:1 #4a00e0);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 15px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #4a00e0, stop:1 #8e2de2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #6a00b8, stop:1 #5a00a0);
            }
        """)

        # Animation for hover in/out effect
        self._animation = QPropertyAnimation(self, b"opacity")
        self._animation.setDuration(200)
        self._animation.setStartValue(0.7)
        self._animation.setEndValue(1.0)
        
    def enterEvent(self, event):
        self._animation.setDirection(QPropertyAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.setDirection(QPropertyAnimation.Backward)
        self._animation.start()
        super().leaveEvent(event)
        
    def getOpacity(self):
        return self._opacity
        
    def setOpacity(self, opacity):
        self._opacity = opacity
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #8e2de2, stop:1 #4a00e0);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 15px;
                margin-top: 5px;
                opacity: {opacity};
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #4a00e0, stop:1 #8e2de2);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #6a00b8, stop:1 #5a00a0);
            }}
        """)

    opacity = pyqtProperty(float, getOpacity, setOpacity)

###############################################################################
#                              DSATracker MAIN                               #
###############################################################################
class DSATracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadData()
        
        # Fade-in animation for the window (maintaining smooth entry)
        self.setWindowOpacity(0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(1000)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(100, self.fade_in_animation.start)
        
        self.updateDailyQuote()
    
    def updateDailyQuote(self):
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            if os.path.exists(JSON_PATH):
                with open(JSON_PATH, 'r') as file:
                    data = json.load(file)
                    if data.get('date') == today and 'quote' in data:
                        self.quote_label.setText(data['quote'])
                        return
        except:
            pass
        # Pick a new random quote if none for today
        quote = random.choice(MOTIVATIONAL_QUOTES)
        self.quote_label.setText(quote)
        self.saveData()
    
    def initUI(self):
        self.setWindowTitle("DSA Progress Tracker - Rishabh Shetty")
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Header: user name & date with improved font sizes for clarity
        self.header_layout = QHBoxLayout()
        self.name_label = QLabel("Rishabh Shetty's DSA Tracker")
        self.name_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.name_label.setStyleSheet("color: #ecf0f1;")
        self.header_layout.addWidget(self.name_label)
        
        self.date_label = QLabel(datetime.now().strftime("%A, %d %B %Y"))
        self.date_label.setFont(QFont("Segoe UI", 16))
        self.date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.date_label.setStyleSheet("color: rgba(236, 240, 241, 0.9);")
        self.header_layout.addWidget(self.date_label)
        
        self.main_layout.addLayout(self.header_layout)
        
        # Quote of the day section with a dark, subtle background
        self.quote_frame = QFrame()
        self.quote_frame.setStyleSheet("""
            QFrame {
                background: #34495e;
                border-radius: 10px;
                margin: 10px 0px;
            }
        """)
        self.quote_layout = QVBoxLayout(self.quote_frame)
        
        self.quote_title = QLabel("Quote of the Day")
        self.quote_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.quote_title.setStyleSheet("color: #8e2de2;")
        self.quote_layout.addWidget(self.quote_title)
        
        self.quote_label = QLabel("Loading today's inspiration...")
        italicFont = QFont("Segoe UI", 12)
        italicFont.setItalic(True)
        self.quote_label.setFont(italicFont)
        self.quote_label.setStyleSheet("color: #ecf0f1;")
        self.quote_label.setWordWrap(True)
        self.quote_layout.addWidget(self.quote_label)
        
        self.main_layout.addWidget(self.quote_frame)
        
        # Main grid layout for left (inputs) & right (progress)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)
        
        ############################
        #       LEFT COLUMN        #
        ############################
        self.left_column = QWidget()
        self.left_layout = QVBoxLayout(self.left_column)
        
        # DSA topic label and input
        self.topic_label = QLabel("Today's DSA Topic")
        self.topic_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.topic_label.setStyleSheet("color: #ecf0f1;")
        self.left_layout.addWidget(self.topic_label)
        
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter the topic you're working on...")
        self.topic_input.setFont(QFont("Segoe UI", 12))
        self.topic_input.setStyleSheet("""
            QLineEdit {
                background: #34495e;
                border: none;
                border-radius: 10px;
                padding: 10px;
                color: #ecf0f1;
            }
            QLineEdit:focus {
                background: #34495e;
            }
        """)
        self.left_layout.addWidget(self.topic_input)
        
        # New question label and input
        self.question_label = QLabel("Add New Question")
        self.question_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.question_label.setStyleSheet("color: #ecf0f1; margin-top: 15px;")
        self.left_layout.addWidget(self.question_label)
        
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Enter a question...")
        self.question_input.setFont(QFont("Segoe UI", 12))
        self.question_input.setStyleSheet("""
            QLineEdit {
                background: #34495e;
                border: none;
                border-radius: 10px;
                padding: 10px;
                color: #ecf0f1;
            }
            QLineEdit:focus {
                background: #34495e;
            }
        """)
        self.left_layout.addWidget(self.question_input)
        
        self.add_button = ButtonWithRipple("Add Question")
        self.add_button.clicked.connect(self.addQuestion)
        self.left_layout.addWidget(self.add_button)
        
        self.questions_label = QLabel("Today's Questions")
        self.questions_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.questions_label.setStyleSheet("color: #ecf0f1; margin-top: 20px;")
        self.left_layout.addWidget(self.questions_label)
        
        # Scroll area for questions with a dark background to harmonize with the theme
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: #2c3e50;
                border: none;
                border-radius: 10px;
            }
            QScrollBar:vertical {
                background: #2c3e50;
                width: 12px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #34495e;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3b5770;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidget(self.scroll_content)
        
        self.left_layout.addWidget(self.scroll_area)
        self.left_layout.setStretch(7, 1)
        
        ############################
        #       RIGHT COLUMN       #
        ############################
        self.right_column = QWidget()
        self.right_layout = QVBoxLayout(self.right_column)
        self.right_layout.setAlignment(Qt.AlignCenter)
        
        self.progress_label = QLabel("Your Progress")
        self.progress_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("color: #ecf0f1; margin-bottom: 20px;")
        self.right_layout.addWidget(self.progress_label)
        
        self.progress_bar = CircularProgressBar()
        self.right_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        
        self.count_label = QLabel("0/0 Questions Completed")
        self.count_label.setFont(QFont("Segoe UI", 14))
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("color: #ecf0f1; margin-top: 20px;")
        self.right_layout.addWidget(self.count_label)
        
        self.motivation_label = QLabel("Let's get started! You can do this!")
        self.motivation_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.motivation_label.setAlignment(Qt.AlignCenter)
        self.motivation_label.setStyleSheet("color: #8e2de2; margin-top: 30px;")
        self.right_layout.addWidget(self.motivation_label)
        
        self.grid_layout.addWidget(self.left_column, 0, 0)
        self.grid_layout.addWidget(self.right_column, 0, 1)
        self.grid_layout.setColumnStretch(0, 3)
        self.grid_layout.setColumnStretch(1, 2)
        
        # Set main window background to a modern vibrant blue–purple gradient with default light text
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #2b5876, stop:1 #4e4376);
                color: #ecf0f1;
            }
        """)
        
        self.questions = []
        self.completed_count = 0
        
        # Allow pressing Enter to add a question
        self.question_input.returnPressed.connect(self.addQuestion)
    
    def addQuestion(self):
        question_text = self.question_input.text().strip()
        if not question_text:
            return
        
        checkbox_widget = AnimatedCheckBox(question_text)
        checkbox_widget.checkbox.stateChanged.connect(self.updateProgress)
        
        self.scroll_layout.addWidget(checkbox_widget)
        self.questions.append(checkbox_widget)
        
        self.question_input.clear()
        self.question_input.setFocus()
        
        self.updateProgress()
        self.saveData()
    
    def updateProgress(self):
        total = len(self.questions)
        completed = sum(1 for q in self.questions if q.checkbox.isChecked())
        
        self.count_label.setText(f"{completed}/{total} Questions Completed")
        
        if total > 0:
            progress = completed / total
            self.progress_bar.setTargetProgress(progress)
        else:
            self.progress_bar.setTargetProgress(0)
            
        if completed == 0 and total == 0:
            self.motivation_label.setText("Let's get started! You can do this!")
        elif completed == 0 and total > 0:
            self.motivation_label.setText("The journey of a thousand miles begins with a single step!")
        elif completed < total:
            self.motivation_label.setText("Keep going! You're making progress!")
        else:
            self.motivation_label.setText("Amazing! You've completed all questions!")
        
        self.saveData()
    
    def loadData(self):
        try:
            if not os.path.exists(JSON_PATH):
                return
            with open(JSON_PATH, 'r') as file:
                data = json.load(file)
            
            today = datetime.now().strftime("%Y-%m-%d")
            if data.get('date') != today:
                return  # Reset for a new day
            
            self.topic_input.setText(data.get('topic', ''))
            if 'quote' in data:
                self.quote_label.setText(data['quote'])
            for q_data in data.get('questions', []):
                checkbox_widget = AnimatedCheckBox(q_data['text'])
                checkbox_widget.checkbox.setChecked(q_data.get('completed', False))
                checkbox_widget.checkbox.stateChanged.connect(self.updateProgress)
                checkbox_widget.setMaximumHeight(50)
                self.scroll_layout.addWidget(checkbox_widget)
                self.questions.append(checkbox_widget)
            self.updateProgress()
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def saveData(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            data = {
                'date': today,
                'topic': self.topic_input.text(),
                'quote': self.quote_label.text(),
                'questions': [
                    {
                        'text': q.checkbox.text(),
                        'completed': q.checkbox.isChecked()
                    } for q in self.questions
                ]
            }
            os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
            with open(JSON_PATH, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

# Main application entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = DSATracker()
    window.show()
    
    sys.exit(app.exec_())
