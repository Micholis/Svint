from SvintTypes.plugin import SvintPlugin
import aiosqlite
import logging
import pathlib
import utils

class school(SvintPlugin):
    def Enable(self):
        self.telegramAvailable = self._pluginAvailable("telegram")

    async def EnableAsync(self):
        self.database = await aiosqlite.connect(pathlib.Path(self.path, "diary.db"))
        logging.info("Successfully connected to database!")

        await self.database.execute('''create table if not exists diary(
                                    Date date, 
                                    Number int, 
                                    Topic test,
                                    Homework text,
                                    Test text,
                                    TopicFiles json,
                                    HomeworkFiles json,
                                    TestFiles json
                                    );''')
        await self.database.commit()

        self._setEventResponder("get_day", self.getDay, True)
        self._registerEvent("set_lesson", True)
        self._addEventListener("school.set_lesson", self.setLesson)

    async def getDay(self, event):
        day = event.params.get("date")
        row = await self.database.execute_fetchall(f"select * from diary where date={day};")
        if row == []: return None
        return row

    async def setLesson(self, event):
        day = event.params.get("date")
        currentLessons = await self.getDay(event)

        lessonName = event.params.get("name")
        lessonNumber = event.params.get("number")

        topic = event.params.get("topic")
        homework = event.params.get("homework")
        test = event.params.get("test")

        topicFiles = event.params.get("topic_files")
        homeworkFiles = event.params.get("homework_files")
        testFiles = event.params.get("test_files")

        if currentLessons is None:
            await self.database.execute(f'''
                insert into diry
                ({"" if topic is None else "Topic"}
                {"" if homework is None else "Homework"}
                {"" if test is None else "Test"}
                {"" if topicFiles is None else "TopicFiles"}
                {"" if homeworkFiles is None else "HomeworkFiles"}
                {"" if testFiles is None else "TestFiles"})
                values
                ({"" if topic is None else f"Topic = {topic}"}
                {"" if homework is None else f"Homework = {homework}"}
                {"" if test is None else f"Test = {test}"}
                {"" if topicFiles is None else f"TopicFiles = {topicFiles}"}
                {"" if homeworkFiles is None else f"HomeworkFiles = {homeworkFiles}"}
                {"" if testFiles is None else f"TestFiles = {testFiles}"})
            ''')
            return

        await self.database.execute(f'''
            update diary set
            {"" if topic is None else f"Topic = {topic}"}
            {"" if homework is None else f"Homework = {homework}"}
            {"" if test is None else f"Test = {test}"}
            {"" if topicFiles is None else f"TopicFiles = {topicFiles}"}
            {"" if homeworkFiles is None else f"HomeworkFiles = {homeworkFiles}"}
            {"" if testFiles is None else f"TestFiles = {testFiles}"}
            where 
            Date = {day}
            Number = {lessonNumber};
        ''')