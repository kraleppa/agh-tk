import React from "react";
import "./SearchBar.css";

function SearchBar({placeholder, data}) {
    return(
        <div className="search">
            <div className="searchInputs">
                <input type="text" placeholder={placeholder} />
            </div>
            <div className="dataResult">
                {data.map((value,key) => {
                    return <div> {value.title} </div>
                })}
            </div>
        </div>
    )
}

export default SearchBar
