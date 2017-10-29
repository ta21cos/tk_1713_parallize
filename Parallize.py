import json
from Dish import Dish, Process

class Cookdule():
    def __init__(self, dishes):
        self.dishes = dishes
        self.observers = [dish.createObserver() for dish in self.dishes]


    def parallize(self):
        dishes = self.dishes
        observers = self.observers

        t = 0
        num_remained_stove = 2
        cooking_dish = 0 # dish number which user cooking 0-len(dishes)
        cook_loaded = False
        procedure = []
        loop = 0

        while True:
            t += 1

            comp = True
            for observer in observers:
                comp &= observer.completed
            if comp == True:
                break

            for i, (dish, observer) in enumerate(zip(dishes, observers)):
                if observer.completed == False:
                    finished, used_cookware, loaded = observer.checkProcessFinished(dish)
                    if finished:
                        procedure.append(("end", i, observer.cooking_process, t))
                        observer.cooking_process += 1

                        if observer.cooking_process == observer.num_process:
                            observer.completed = True

                        if used_cookware is not None:
                            if used_cookware:
                                num_remained_stove += 1

                        if loaded is not None:
                            if loaded:
                                cook_loaded = False

            for i, (dish, observer) in enumerate(zip(dishes, observers)):
                if observer.completed == False and \
                        observer.is_cooking == False:
                    print(i, observer.completed, observer.cooking_process)
                    if dish.procedure[observer.cooking_process].needStove() and num_remained_stove == 0:
                        continue
                    if dish.procedure[observer.cooking_process].isLoadingWork() and cook_loaded == True:
                        continue

                    observer.is_cooking = True
                    if dish.procedure[observer.cooking_process].needStove():
                        num_remained_stove -= 1
                        if num_remained_stove < 0:
                            print("remained_stove_error")
                            exit(-1)
                    if dish.procedure[observer.cooking_process].isLoadingWork():
                        cook_loaded = not cook_loaded
                        if cook_loaded == False:
                            print("cook_loaded_error")
                            exit(-1)

                    procedure.append(("start", i, observer.cooking_process, t))

            # 時間経過
            for observer in observers:
                if observer.is_cooking == True:
                    observer.remained_time[observer.cooking_process] -= 1
            for observer in observers:
                print(observer.is_cooking, observer.cooking_process, observer.remained_time, observer.completed)
            print("")

            # if loop==10:
             #    break
        print(procedure)
        self.procedure = procedure

    def getDishName(self, dish_idx):
        return self.dishes[dish_idx].name

    def getDishId(self, dish_idx):
        return self.dishes[dish_idx].recipe_id

    def getCookDescription(self, dish_idx, process_idx):
        return self.dishes[dish_idx].procedure[process_idx].description

    def getCookDuration(self, dish_idx, process_idx):
        return self.dishes[dish_idx].procedure[process_idx].time

    def displayProcedure(self):
        if self.procedure is None:
            print("run parallize() before displaying")
            return

        process_idx = 0
        t = 0
        while True:
            process = self.procedure[process_idx]
            if process[3] == t:
                print("t =", t, end=" ")
                print(process[0], end=", ")
                print(self.getDishName(process[1]), end=", ")
                print(self.getCookDescription(process[1], process[2]))
                process_idx += 1
                if process_idx == len(self.procedure):
                    break
            else:
                print("|")
                t += 1

    def exportProcedure(self):
        if self.procedure is None:
            print("run parallize() before displaying")
            return

        content = []
        for i, process in enumerate(self.procedure):
            content.append({"index": i, "description": self.getCookDescription(process[1], process[2]), "duration": self.getCookDuration(process[1], process[2]), "mo_start": 0, "mo_end": 0, "recipe_id": self.getDishId(process[1])})

        _json = {"result": content}
        with open("procedure.json", "w") as f:
            json.dump(_json, f)
        print(_json)
        return _json


def main_test():
    dish1 = Dish.addTestProcedure("nikujaga")
    dish2 = Dish.addTestProcedure("karaage")

    # parallize([dish1, dish2], [dish1_obs, dish2_obs])

    cookdule = Cookdule([dish1, dish2])
    cookdule.parallize()
    cookdule.displayProcedure()
    cookdule.exportProcedure()

def main_db():
    dish1 = Dish()
    dish1.getRecipe(3)
    print(dish1.procedure[0].time)
    dish2 = Dish()
    dish2.getRecipe(10)

    cookdule = Cookdule([dish1, dish2])
    cookdule.parallize()
    cookdule.displayProcedure()
    cookdule.exportProcedure()

def main(recipe_ids):
    dishes = []
    for recipe_id in recipe_ids:
        dish = Dish()
        dish.getRecipe(recipe_id)
        dishes.append(dish)

    cookdule = Cookdule(dishes)
    cookdule.parallize()
    return cookdule.exportProcedure()


if __name__ == "__main__":
    main_db()
