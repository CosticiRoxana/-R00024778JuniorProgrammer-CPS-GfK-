SELECT
    p.Locatie,
    p.First_Name,
    p.Last_Name,
    COUNT(v.ID) AS Total_Votes,
    GROUP_CONCAT(DISTINCT v.quality) AS Qualities
FROM
    persons p
LEFT JOIN
    votes v ON p.ID = v.chosen_person
GROUP BY
    p.Locatie,
    p.First_Name,
    p.Last_Name;

