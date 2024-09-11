import CreateBook from "./my_comp/CreateBook";
import BookCard from "./my_comp/BookCard";

const Home = () => {
    return (
        <div className="p-6 max-w-4xl mx-auto">
            <CreateBook />
            <div className="border rounded">
                <BookCard />
            </div>
         </div>
    )
  }

export default Home;