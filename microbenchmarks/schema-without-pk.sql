CREATE TABLE Comment (
    creationDate TIMESTAMP WITH TIME ZONE NOT NULL,
    id BIGINT NOT NULL,
    locationIP TEXT NOT NULL,
    browserUsed TEXT NOT NULL,
    content TEXT NOT NULL,
    length INT NOT NULL,
    CreatorPersonId BIGINT NOT NULL,
    LocationCountryId BIGINT NOT NULL,
    ParentPostId BIGINT,
    ParentCommentId BIGINT,
);
