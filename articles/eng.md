Today I want to introduce to you a new [Beanie](https://github.com/roman-right/beanie) feature. MongoDB projections are supported now. It helps to reduce database load and makes your services more efficient.

How does it work? You can set up two document models for the same collection:
- A big one - for the regular operations
- A short one - for the case, when you need only a few fields

Beanie is using MongoDB projections when it takes the data from the database. It means it is asking only the data, which was described in the model. Not filtering results but asking for limited data. This is reducing, and database load, and network load.

I will show on small FastAPI service example:

This is an ice cream store api. It has an Ice Cream entity. To create and get single ice cream I will use the long model:

```python
class Nutrition(BaseModel):
    energy: float
    fat: float
    protein: float
    carbs: float


class IceCream(Document):
    name: str
    price: float
    summary: str
    description: str
    ingredients: List[str]
    per_100_gr: Nutrition

    class Collection:
        name = "ice-cream"
```

And to return the list of the ice creams I'll use the short version:

```python
class IceCreamShort(Document):
    name: str
    price: float
    summary: str

    class Collection:
        name = "ice-cream"
```

And the endpoints are neat as usual with FastAPI:

```python
# CREATE ICE CREAM

@ice_cream_router.post("/", response_model=IceCream)
async def new(ice_cream: IceCream):
    await ice_cream.create()
    return ice_cream

# GET SINGLE ICE CREAM

@ice_cream_router.get("/{ice_cream_id}", response_model=IceCream)
async def get(ice_cream_id: PydanticObjectId):
    ice_cream = await IceCream.get(ice_cream_id)
    if ice_cream is None:
        raise HTTPException(status_code=404, detail="Ice cream not found")
    return ice_cream

# GET LIST OF ALL THE AVAILABLE ICE CREAMS

@ice_cream_router.get("/", response_model=List[IceCreamShort])
async def get_list():
    print(await IceCreamShort.find_all().to_list())
    return await IceCreamShort.find_all().to_list()
```

Let's test. For the list endpoint it returns next:

```json
[
    {
        "_id": "607fe424447d1f704c7b12ea",
        "name": "Ben & Jerry's Netflix & Chill'd",
        "price": 7.0,
        "summary": "Peanut Butter Dairy Ice Cream with Sweet & Salty Pretzel Swirls & Brownie Pieces"
    },
    {
        "_id": "607fe670447d1f704c7b12eb",
        "name": "Chip Happens",
        "price": 6.0,
        "summary": "A Cold Mess of Chocolate Ice Cream with Chocolatey Chips & Crunchy Potato Chip Swirls"
    }
]
```

While for the single ice cream information it gives this:

```json
{
    "_id": "607fe670447d1f704c7b12eb",
    "name": "Chip Happens",
    "price": 6.0,
    "summary": "A Cold Mess of Chocolate Ice Cream with Chocolatey Chips & Crunchy Potato Chip Swirls",
    "description": "Sometimes “chip” happens and everything’s a mess, but we Nailed It! with this chip-filled limited batch. When smooth chocolate ice cream meets chocolatey chips & salty swirls, they pack a serious one-two crunch. The best part? There won’t be anything left to clean up.",
    "ingredients": [
        "Cream (MILK) (26%)",
        "water",
        "condensed skimmed MILK",
        "sugar",
        "vegetable oils (coconut, fully refined soybean, sunflower)",
        "glucose syrup",
        "potatoes",
        "cocoa powder (1.5%)",
        "starch",
        "fat reduced cocoa powder (1%)",
        "free range EGG yolk",
        "vanilla extract",
        "salt",
        "emulsifier (SOY lecithin)",
        "stabilisers (guar gum, carrageenan)",
        "MILK fat",
        "natural vanilla flavouring. Sugar, cocoa, vanilla: mass balance is used to match Fairtrade sourcing, total 20% F. F Visit info.fairtrade.net/sourcing"
    ],
    "per_100_gr": {
        "energy": 277.0,
        "fat": 17.0,
        "protein": 3.7,
        "carbs": 27.0
    }
}
```

In this case, it reduces database and network loads several times for the list view.

The whole working project can be found by [link](https://github.com/roman-right/ice-cream-store)

Links:

- [Beanie](https://github.com/roman-right/beanie)
- [Demo Project](https://github.com/roman-right/ice-cream-store)