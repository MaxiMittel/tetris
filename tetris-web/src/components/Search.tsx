import React, { useEffect, useState } from "react";
import { search } from "../api/search";

interface Props {}

export const Search: React.FC<Props> = (props: Props) => {
  type Result = {
    id: string;
    name: string;
    highscore: number;
  };

  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Result[]>([]);

  useEffect(() => {
    if (query.length > 0) {
      search(query)
        .then((response) => {
          setResults(response.data);
        })
        .catch(() => {
          setResults([]);
        });
    }
  }, [query]);

  return (
    <div className="container-sm" style={{ padding: "2em" }}>
      <input
        type="text"
        className="form-control"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      ></input>
      <div className="searchResultsContainer">
        {results.length <= 0 && <p className="noResults">No results found.</p>}
        {results.map((result) => (
          <SearchResult
            name={result.name}
            highscore={result.highscore}
            id={result.id}
          />
        ))}
      </div>
    </div>
  );
};

interface SearchResultsProps {
  name: string;
  highscore: number;
  id: string;
}

const SearchResult: React.FC<SearchResultsProps> = (
  props: SearchResultsProps
) => {
  return (
    <div className="w-400 mw-full">
      <div className="card">
        <h2 className="card-title">{props.name}</h2>
        <p>
          Highscore :{" "}
          <span className="badge badge-primary">{props.highscore}</span>
        </p>
        <div className="text-right">
          <a href={`user/${props.id}`} className="btn btn-primary">
            Profile
          </a>
        </div>
      </div>
    </div>
  );
};
