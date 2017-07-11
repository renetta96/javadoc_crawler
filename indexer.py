from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from javadoc.enums import Version
import traceback

Base = declarative_base()

engine = create_engine("mysql://root@localhost/javadoc")

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

parents = {
    Version.JAVA6: 'java6',
    Version.JAVA7: 'java7',
    Version.JAVA8: 'java8'
}

files_to_read = ['classes_java6.jl', 'classes_java7.jl', 'classes_java8.jl',
                 'packages_java6.jl', 'packages_java7.jl', 'packages_java8.jl']


class JavaDoc(Base):
    __tablename__ = 'javadoc'
    name = Column(String(100), primary_key=True)
    parent = Column(String(100), primary_key=True)
    url = Column(String(500, collation='utf8_bin'), primary_key=True)
    version = Column(String(10), primary_key=True)
    type = Column(String(20))
    parent_type = Column(String(20))


def get_length_for_fields():
    field_length = {
        'name': [0, ''],
        'parent': [0, ''],
        'url': [0, ''],
        'type': [0, ''],
        'parent_type': [0, '']
    }

    for file_name in files_to_read:
        print 'Reading file ' + file_name
        with open(file_name, 'r') as f:
            for line in f.readlines():
                obj = json.loads(line)

                for k in field_length:
                    if isinstance(obj[k], basestring) and len(obj[k]) > field_length[k][0]:
                        field_length[k][0] = len(obj[k])
                        field_length[k][1] = obj[k]

    return field_length


def index_from_file(file_name, offset=0, limit=-1):
    print 'Indexing from file ', file_name
    with open(file_name, 'r') as f:
        count = 0
        for line in f.readlines():
            if count < offset:
                continue

            obj = json.loads(line)
            assert obj['version'] in Version.get_list()
            assert obj['name'] is not None
            assert obj['url'] is not None

            if obj['parent'] is None:
                obj['parent'] = parents[obj['version']]

            jdoc = JavaDoc(name=obj['name'], parent=obj['parent'],
                           url=obj['url'], version=obj['version'],
                           type=obj['type'], parent_type=obj['parent_type'])
            try:
                session.merge(jdoc)
                session.commit()
            except Exception as e:
                print "Exception at line ", count
                raise e

            count += 1
            if count >= limit >= 0:
                break

    print 'Finished indexing from file ', file_name

if __name__ == '__main__':
    print get_length_for_fields()
    # for file_name in files_to_read:
    #     index_from_file(file_name)
    #
    # session.close()

    # Fix type bugs in some records
    # docs = session.query(JavaDoc).filter((JavaDoc.type == '') | (JavaDoc.parent_type == '')).all()
    # for doc in docs:
    #     assert (doc.type == '') or (doc.parent_type == '')
    #     if doc.type == '':
    #         assert doc.name == 'Class'
    #         doc.type = 'Class'
    #         session.commit()
    #
    #     if doc.parent_type == '':
    #         assert doc.parent == 'java.lang.Class'
    #         doc.parent_type = 'Class'
    #         session.commit()
    #
    # session.close()

    # Find duplicates or missing rows
    # url_set = set()
    # with open('classes_java8.jl', 'r') as f:
    #     # docs = session.query(JavaDoc).filter(JavaDoc.version == Version.JAVA8)\
    #     #     .filter(JavaDoc.type != 'Package').all()
    #     #
    #     # print len(docs)
    #     #
    #     # for doc in docs:
    #     #     url_set.add(doc.url)
    #
    #     # print len(url_set)
    #
    #     lines = f.readlines()
    #     print len(lines)
    #     for line in lines:
    #         obj = json.loads(line)
    #         if obj['parent'] is None:
    #             obj['parent'] = parents[obj['version']]
    #
    #         if obj['url'] in url_set:
    #             print obj
    #             # jdoc = JavaDoc(name=obj['name'], parent=obj['parent'],
    #             #                url=obj['url'], parent_type=obj['parent_type'],
    #             #                type=obj['type'], version=obj['version'])
    #             #
    #             # session.add(jdoc)
    #             # session.commit()
    #         else:
    #             url_set.add(obj['url'])
    #
    # session.close()







