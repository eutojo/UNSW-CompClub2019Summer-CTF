from .SQLQuery import SQLQuery
from .. import database


def assertSQLResult(result):
    result = all(result)
    if result:
        database.conn.commit()
    else:
        database.conn.rollback()
    return result


class SQLMethod:
    # User Functions
    @staticmethod
    def solveQuestion(user: int, question: int):
        return database.insert(SQLQuery.solves.add, (user, question))

    # Admin functions
    @staticmethod
    def unsolveQuestion(user: int, question: int):
        return database.update(SQLQuery.solves.deleteSpecific, (user, question))

    @staticmethod
    def createQuestion(title: str, description: str, flag: str, value: int, category: int):
        return database.insert(SQLQuery.questions.add, (title, description, flag, value, category))

    @staticmethod
    def editQuestion(question: int, title: str, description: str, value: int, category: int):
        return database.update(SQLQuery.questions.edit, (title, description, value, category, question))

    @staticmethod
    def editQuestionFlag(question: int, flag: str):
        return database.update(SQLQuery.questions.editFlag, (flag, question))

    @staticmethod
    def deleteQuestion(question: int):
        result = []
        result.append(database.update(SQLQuery.questions.delete, (question,), commit = False))
        result.append(database.update(SQLQuery.solves.deleteQuestion, (question,), commit = False))

        return assertSQLResult(result)

    @staticmethod
    def deleteUser(user: int):
        return database.update(SQLQuery.solves.deleteUser, (user,))

    # result = []
    # result.append(database.update(UserSQL.delete, (user,), commit=False))
    # result.append(database.update(SQLQuery.solves.deleteUser, (user,), commit=False))
    # return assertSQLResult(result)

    # Helper functions
    @staticmethod
    def getFlag(question: int):
        return database.fetchOne(SQLQuery.questions.getFlag, (question,))

    @staticmethod
    def getSolves(*, user: int = None, question: int = None):
        if not any([user, question]):
            database.fetchAll(SQLQuery.solves.getAll)
        elif user is not None:
            database.fetchAll(SQLQuery.solves.getUser, (user,))
        else:  # question is not None
            database.fetchAll(SQLQuery.solves.getQuestion, (question,))

    @staticmethod
    def getQuestions(*, question: int = None, flag: bool = False):
        if question:
            if flag:
                return database.fetchOne(SQLQuery.questions.getOneWithFlag, (question,))
            else:
                return database.fetchOne(SQLQuery.questions.getOne, (question,))
        else:  # get all
            if flag:
                return database.fetchAll(SQLQuery.questions.getAllWithFlag, (question,))
            else:
                return database.fetchAll(SQLQuery.questions.getAll, (question,))

    getQuestion = getQuestions