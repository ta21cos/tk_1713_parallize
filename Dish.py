import psycopg2

class Dish():
    def __init__(self):
        self.name = ""
        self.procedure = []
        self.num_process = 0

    def getProcedure(self):
        return self.procedure

    def addProcess(self, process):
        self.procedure.append(process)
        self.num_process += 1

    def createObserver(self):
        return Observer(self)

    def getRecipe(self, recipe_id):
        conn = psycopg2.connect("dbname=recipe_development host=localhost user=tellusium")
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipes where id = (%s);", [recipe_id])
        recipe = cur.fetchone()
        print(recipe)
        self.recipe_id = recipe[0]
        self.name = recipe[1]


        cur.execute("select * from cooking_processes where recipe_id = (%s);", [recipe_id])
        processes = cur.fetchall()
        print(processes)
        for process in processes:
            step_no = process[1]
            description = process[2]
            cookware = process[4]
            parallel = process[5]
            duration = process[6] if process[6] > 0.5 else 3
            movie_start = process[7]
            movie_end = process[8]
            _process = Process(step_no, description, cookware, parallel, duration, movie_start, movie_end)
            self.addProcess(_process)


class Observer():
    def __init__(self, dish):
        self.completed = False
        self.is_cooking = False
        self.cooking_process = 0
        self.num_process = dish.num_process
        self.remained_time = [process.time for process in dish.procedure]

    def checkCookingCompleted(self):
        if self.cooking_process == self.num_process - 1:
            self.completed = True
            return True
        return False

    def checkProcessFinished(self, dish):
        if self.remained_time[self.cooking_process] == 0:
            used_cookware = dish.procedure[self.cooking_process].cookware
            load = not dish.procedure[self.cooking_process].parallel

            self.is_cooking = False
            return True, used_cookware, load # どれか一つしかtime==0にならないのでここでreturn
        return False, None, None


class Process():
    def __init__(self, step_no, description, cookware, parallel, time, movie_start, movie_end):
        self.step_no = step_no
        self.description = description
        self.cookware = cookware
        self.parallel = parallel
        self.time = time
        self.movie_start = movie_start
        self.movie_end = movie_end

    def needStove(self):
        if self.cookware:
            return True
        return False

    def isLoadingWork(self):
        if self.parallel == True:
            return False
        return True

    @classmethod
    def createProcessArrayFromJsonArray(cls, arr):
        processes = []
        for dic in arr:
            process = cls(dic["step_no"], dic["description"], dic["ingredient"], dic["work"], dic["cookware"], dic["parallel"], dic["time"])
            processes.append(process)
        return processes

if __name__ == "__main__":
    dish = Dish()
    dish.getRecipe(3)
    print(dish.procedure)
    exit(-1)
    dish.addTestProcedure("nikujaga")

    for process in dish.procedure:
        print(process.description)
