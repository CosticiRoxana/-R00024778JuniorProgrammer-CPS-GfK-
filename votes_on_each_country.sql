SELECT
    p.Locatie AS Country,
    COUNT(v.ID) AS Total_Votes
FROM
    persons p
LEFT JOIN
    votes v ON p.ID = v.chosen_person
GROUP BY
    p.Locatie;
